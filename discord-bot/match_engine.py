"""
Match Engine — The heartbeat of the stadium.
Polls live match data (or simulates) and emits events to all agents.

Events emitted:
  match_prematch(minutes_to_kickoff)
  match_kickoff()
  match_goal(team, scorer, minute, score_home, score_away)
  match_card(team, player, card_type, minute)
  match_halftime(score_home, score_away)
  match_second_half()
  match_fulltime(score_home, score_away)
  match_stats_update(stats_dict)
"""

import asyncio
import random
import time
from datetime import datetime, timezone, timedelta
from discord.ext import commands, tasks
import config


class MatchState:
    """Tracks current match state."""

    def __init__(self):
        self.status = "pre_match"  # pre_match, live_1h, halftime, live_2h, finished
        self.minute = 0
        self.home_team = config.MATCH_HOME_TEAM
        self.away_team = config.MATCH_AWAY_TEAM
        self.score_home = 0
        self.score_away = 0
        self.events = []  # list of match events
        self.stats = {
            "possession_home": 50, "possession_away": 50,
            "shots_home": 0, "shots_away": 0,
            "shots_on_target_home": 0, "shots_on_target_away": 0,
            "corners_home": 0, "corners_away": 0,
            "fouls_home": 0, "fouls_away": 0,
            "yellow_cards_home": 0, "yellow_cards_away": 0,
            "red_cards_home": 0, "red_cards_away": 0,
        }
        self.kickoff_time = None
        self._sim_last_minute = -1

    @property
    def score_line(self):
        return f"{self.home_team} {self.score_home} - {self.score_away} {self.away_team}"

    @property
    def is_live(self):
        return self.status in ("live_1h", "live_2h")


class MatchEngine(commands.Cog):
    """
    Core engine that drives the match.
    In 'simulate' mode, generates realistic match events for testing.
    In 'live' mode, polls API-Football for real data.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.state = MatchState()
        self.mode = config.MATCH_API_MODE
        self._prematch_alerts_sent = set()

        # Calculate kickoff time
        date_parts = config.MATCH_DATE.split("-")
        time_parts = config.MATCH_TIME_UTC.split(":")
        self.state.kickoff_time = datetime(
            int(date_parts[0]), int(date_parts[1]), int(date_parts[2]),
            int(time_parts[0]), int(time_parts[1]),
            tzinfo=timezone.utc
        )

    async def cog_load(self):
        self.engine_loop.start()

    def cog_unload(self):
        self.engine_loop.cancel()

    @tasks.loop(seconds=10)
    async def engine_loop(self):
        """Main engine tick — runs every 10 seconds."""
        now = datetime.now(timezone.utc)
        minutes_to_kickoff = (self.state.kickoff_time - now).total_seconds() / 60

        if self.state.status == "pre_match":
            await self._handle_prematch(minutes_to_kickoff)
        elif self.state.status in ("live_1h", "live_2h"):
            if self.mode == "simulate":
                await self._simulate_tick()
            else:
                await self._live_tick()
        elif self.state.status == "halftime":
            pass  # Wait for second half trigger

    @engine_loop.before_loop
    async def before_engine(self):
        await self.bot.wait_until_ready()
        print(f"[MatchEngine] Started in '{self.mode}' mode")
        print(f"[MatchEngine] Kickoff: {self.state.kickoff_time.isoformat()}")

    # ── Pre-match ────────────────────────────────────

    async def _handle_prematch(self, minutes_to_kickoff):
        if minutes_to_kickoff <= 0:
            self.state.status = "live_1h"
            self.state.minute = 0
            self.bot.dispatch("match_kickoff")
            return

        for interval in config.COUNTDOWN_INTERVALS:
            if minutes_to_kickoff <= interval and interval not in self._prematch_alerts_sent:
                self._prematch_alerts_sent.add(interval)
                self.bot.dispatch("match_prematch", interval)

    # ── Simulation Mode ──────────────────────────────

    async def _simulate_tick(self):
        """Advance the simulated match by ~1 minute per tick."""
        self.state.minute += 1
        minute = self.state.minute

        # Halftime
        if minute == 45 and self.state.status == "live_1h":
            self.state.status = "halftime"
            self.bot.dispatch("match_halftime", self.state.score_home, self.state.score_away)
            # Auto-resume after 60 seconds (simulated halftime)
            await asyncio.sleep(60)
            self.state.status = "live_2h"
            self.state.minute = 45
            self.bot.dispatch("match_second_half")
            return

        # Full time
        if minute >= 90 and self.state.status == "live_2h":
            self.state.status = "finished"
            self.bot.dispatch("match_fulltime", self.state.score_home, self.state.score_away)
            self.engine_loop.cancel()
            return

        # Random events
        roll = random.random()

        # ~8% chance of a goal per minute
        if roll < 0.08:
            is_home = random.random() < 0.55
            scorers_home = ["Bailey", "Antonio", "Nicholson", "Reid", "Lowe"]
            scorers_away = ["Hmae", "Wacapo", "Gope-Fenepej", "Cawa"]
            if is_home:
                self.state.score_home += 1
                scorer = random.choice(scorers_home)
                team = self.state.home_team
            else:
                self.state.score_away += 1
                scorer = random.choice(scorers_away)
                team = self.state.away_team
            self.bot.dispatch(
                "match_goal", team, scorer, minute,
                self.state.score_home, self.state.score_away
            )

        # ~5% chance of a yellow card
        elif roll < 0.13:
            is_home = random.random() < 0.5
            team = self.state.home_team if is_home else self.state.away_team
            players_home = ["Powell", "Lawrence", "Moore", "Bell"]
            players_away = ["Wajoka", "Sihaze", "Kaluak"]
            player = random.choice(players_home if is_home else players_away)
            if is_home:
                self.state.stats["yellow_cards_home"] += 1
            else:
                self.state.stats["yellow_cards_away"] += 1
            self.bot.dispatch("match_card", team, player, "yellow", minute)

        # Update stats every tick
        self.state.stats["possession_home"] = random.randint(45, 65)
        self.state.stats["possession_away"] = 100 - self.state.stats["possession_home"]
        if random.random() < 0.15:
            if random.random() < 0.55:
                self.state.stats["shots_home"] += 1
                if random.random() < 0.4:
                    self.state.stats["shots_on_target_home"] += 1
            else:
                self.state.stats["shots_away"] += 1
                if random.random() < 0.35:
                    self.state.stats["shots_on_target_away"] += 1
        if random.random() < 0.08:
            if random.random() < 0.5:
                self.state.stats["corners_home"] += 1
            else:
                self.state.stats["corners_away"] += 1
        if random.random() < 0.12:
            if random.random() < 0.5:
                self.state.stats["fouls_home"] += 1
            else:
                self.state.stats["fouls_away"] += 1

        # Emit stats update every 15 minutes
        if minute % config.STATS_INTERVAL_MINUTES == 0 and minute != self.state._sim_last_minute:
            self.state._sim_last_minute = minute
            self.bot.dispatch("match_stats_update", self.state.stats.copy())

    # ── Live API Mode ────────────────────────────────

    async def _live_tick(self):
        """Poll real match data from API-Football."""
        try:
            import aiohttp
            headers = {
                "X-RapidAPI-Key": config.MATCH_API_KEY,
                "X-RapidAPI-Host": config.MATCH_API_HOST,
            }
            url = f"https://{config.MATCH_API_HOST}/v3/fixtures"
            params = {"id": config.MATCH_FIXTURE_ID}

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as resp:
                    data = await resp.json()

            fixture = data["response"][0]
            new_minute = fixture["fixture"]["status"]["elapsed"] or 0
            status_short = fixture["fixture"]["status"]["short"]

            # Detect goals
            new_home = fixture["goals"]["home"] or 0
            new_away = fixture["goals"]["away"] or 0

            if new_home > self.state.score_home:
                self.state.score_home = new_home
                self.bot.dispatch(
                    "match_goal", self.state.home_team, "Unknown", new_minute,
                    new_home, new_away
                )
            if new_away > self.state.score_away:
                self.state.score_away = new_away
                self.bot.dispatch(
                    "match_goal", self.state.away_team, "Unknown", new_minute,
                    new_home, new_away
                )

            # Detect halftime / fulltime
            if status_short == "HT" and self.state.status == "live_1h":
                self.state.status = "halftime"
                self.bot.dispatch("match_halftime", new_home, new_away)
            elif status_short == "2H" and self.state.status == "halftime":
                self.state.status = "live_2h"
                self.bot.dispatch("match_second_half")
            elif status_short in ("FT", "AET", "PEN") and self.state.status != "finished":
                self.state.status = "finished"
                self.bot.dispatch("match_fulltime", new_home, new_away)
                self.engine_loop.cancel()

            self.state.minute = new_minute

            # Update stats from API
            stats_data = fixture.get("statistics", [])
            if stats_data:
                self._parse_api_stats(stats_data)
                if new_minute % config.STATS_INTERVAL_MINUTES == 0:
                    self.bot.dispatch("match_stats_update", self.state.stats.copy())

        except Exception as e:
            print(f"[MatchEngine] API error: {e}")

    def _parse_api_stats(self, stats_data):
        """Parse API-Football statistics into our stats dict."""
        mapping = {
            "Ball Possession": ("possession_home", "possession_away"),
            "Total Shots": ("shots_home", "shots_away"),
            "Shots on Goal": ("shots_on_target_home", "shots_on_target_away"),
            "Corner Kicks": ("corners_home", "corners_away"),
            "Fouls": ("fouls_home", "fouls_away"),
            "Yellow Cards": ("yellow_cards_home", "yellow_cards_away"),
            "Red Cards": ("red_cards_home", "red_cards_away"),
        }
        for team_stats in stats_data:
            is_home = team_stats["team"]["name"] == self.state.home_team
            for stat in team_stats["statistics"]:
                if stat["type"] in mapping:
                    key = mapping[stat["type"]][0 if is_home else 1]
                    val = stat["value"]
                    if isinstance(val, str) and val.endswith("%"):
                        val = int(val.replace("%", ""))
                    self.state.stats[key] = val or 0

    # ── Manual Controls (for testing) ────────────────

    @commands.command(name="sim_goal")
    @commands.has_permissions(administrator=True)
    async def sim_goal(self, ctx, team: str = "home"):
        """Manually trigger a goal event for testing."""
        if team == "home":
            self.state.score_home += 1
            self.bot.dispatch(
                "match_goal", self.state.home_team, "Test Player",
                self.state.minute, self.state.score_home, self.state.score_away
            )
        else:
            self.state.score_away += 1
            self.bot.dispatch(
                "match_goal", self.state.away_team, "Test Player",
                self.state.minute, self.state.score_home, self.state.score_away
            )
        await ctx.send(f"⚽ Simulated goal for {team}. Score: {self.state.score_line}")

    @commands.command(name="sim_kickoff")
    @commands.has_permissions(administrator=True)
    async def sim_kickoff(self, ctx):
        """Manually trigger kickoff for testing."""
        self.state.status = "live_1h"
        self.state.minute = 0
        self.state.kickoff_time = datetime.now(timezone.utc)
        self.bot.dispatch("match_kickoff")
        await ctx.send("🟢 Simulated KICKOFF!")

    @commands.command(name="sim_halftime")
    @commands.has_permissions(administrator=True)
    async def sim_halftime(self, ctx):
        """Manually trigger halftime."""
        self.state.status = "halftime"
        self.bot.dispatch("match_halftime", self.state.score_home, self.state.score_away)
        await ctx.send("⏸️ Simulated HALFTIME!")

    @commands.command(name="sim_fulltime")
    @commands.has_permissions(administrator=True)
    async def sim_fulltime(self, ctx):
        """Manually trigger fulltime."""
        self.state.status = "finished"
        self.bot.dispatch("match_fulltime", self.state.score_home, self.state.score_away)
        await ctx.send("🏁 Simulated FULL TIME!")


async def setup(bot: commands.Bot):
    await bot.add_cog(MatchEngine(bot))
