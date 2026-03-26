"""
STAT MAN — The Analyst Agent
Drops live stats, fun facts, and tactical breakdowns.
"""

import json
import os
import random
import discord
from discord.ext import commands
import config


FACTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "facts.json")


class StatManAgent(commands.Cog):
    """Live stats, fun facts, and match analysis."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.facts = self._load_facts()
        self.facts_used = set()

    def _load_facts(self):
        try:
            with open(FACTS_PATH, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _channel(self):
        for guild in self.bot.guilds:
            for ch in guild.text_channels:
                if ch.name == config.CHANNELS["matchday"]:
                    return ch
        return None

    def _random_fact(self):
        available = [f for i, f in enumerate(self.facts) if i not in self.facts_used]
        if not available:
            self.facts_used.clear()
            available = self.facts
        if not available:
            return None
        fact = random.choice(available)
        self.facts_used.add(self.facts.index(fact))
        return fact

    # ── Pre-match Stats ──────────────────────────────

    @commands.Cog.listener()
    async def on_match_prematch(self, minutes: int):
        if minutes != 30:
            return

        ch = self._channel()
        if not ch:
            return

        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM
        away = engine.state.away_team if engine else config.MATCH_AWAY_TEAM

        await ch.send(
            f"# {config.STATMAN_PREFIX} PRE-MATCH BRIEFING\n\n"
            f"**{home} vs {away}**\n\n"
            f"**{home}:**\n"
            f"- FIFA Ranking: 57th\n"
            f"- Key Player: Michail Antonio (West Ham)\n"
            f"- Form: W-W-D-L-W (last 5)\n"
            f"- Style: Physical, direct, pace on the wings\n\n"
            f"**{away}:**\n"
            f"- FIFA Ranking: 161st\n"
            f"- Key Player: Bertrand Kai (local league)\n"
            f"- Form: W-W-W-D-W (OFC qualifiers)\n"
            f"- Style: Organized defense, counter-attacks\n\n"
            f"**Head-to-Head:** First ever meeting!\n\n"
            f"*This is history being written tonight.*"
        )

    # ── Live Stats Update ────────────────────────────

    @commands.Cog.listener()
    async def on_match_stats_update(self, stats: dict):
        ch = self._channel()
        if not ch:
            return

        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM
        away = engine.state.away_team if engine else config.MATCH_AWAY_TEAM
        minute = engine.state.minute if engine else "?"

        fact = self._random_fact()
        fact_line = f"\n\n💡 *{fact}*" if fact else ""

        await ch.send(
            f"## {config.STATMAN_PREFIX} Match Stats — {minute}'\n\n"
            f"```\n"
            f"{'':>20} {home:>10}  {away:>10}\n"
            f"{'Possession':>20} {stats.get('possession_home', 0):>9}%  {stats.get('possession_away', 0):>9}%\n"
            f"{'Shots':>20} {stats.get('shots_home', 0):>10}  {stats.get('shots_away', 0):>10}\n"
            f"{'On Target':>20} {stats.get('shots_on_target_home', 0):>10}  {stats.get('shots_on_target_away', 0):>10}\n"
            f"{'Corners':>20} {stats.get('corners_home', 0):>10}  {stats.get('corners_away', 0):>10}\n"
            f"{'Fouls':>20} {stats.get('fouls_home', 0):>10}  {stats.get('fouls_away', 0):>10}\n"
            f"{'Yellow Cards':>20} {stats.get('yellow_cards_home', 0):>10}  {stats.get('yellow_cards_away', 0):>10}\n"
            f"```"
            f"{fact_line}"
        )

    # ── Goal Stats ───────────────────────────────────

    @commands.Cog.listener()
    async def on_match_goal(self, team, scorer, minute, score_home, score_away):
        ch = self._channel()
        if not ch:
            return

        engine = self.bot.get_cog("MatchEngine")
        stats = engine.state.stats if engine else {}

        await ch.send(
            f"{config.STATMAN_PREFIX} **Goal Stats — {minute}'**\n"
            f"Shots: {stats.get('shots_home', 0)}-{stats.get('shots_away', 0)} | "
            f"On Target: {stats.get('shots_on_target_home', 0)}-{stats.get('shots_on_target_away', 0)} | "
            f"Possession: {stats.get('possession_home', 50)}%-{stats.get('possession_away', 50)}%"
        )

    # ── Full Time Stats Card ─────────────────────────

    @commands.Cog.listener()
    async def on_match_fulltime(self, score_home, score_away):
        ch = self._channel()
        if not ch:
            return

        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM
        away = engine.state.away_team if engine else config.MATCH_AWAY_TEAM
        stats = engine.state.stats if engine else {}

        total_corners = stats.get("corners_home", 0) + stats.get("corners_away", 0)

        await ch.send(
            f"# {config.STATMAN_PREFIX} FULL TIME STATS CARD\n\n"
            f"## {home} {score_home} - {score_away} {away}\n\n"
            f"```\n"
            f"{'':>20} {home:>10}  {away:>10}\n"
            f"{'─' * 42}\n"
            f"{'Possession':>20} {stats.get('possession_home', 0):>9}%  {stats.get('possession_away', 0):>9}%\n"
            f"{'Total Shots':>20} {stats.get('shots_home', 0):>10}  {stats.get('shots_away', 0):>10}\n"
            f"{'On Target':>20} {stats.get('shots_on_target_home', 0):>10}  {stats.get('shots_on_target_away', 0):>10}\n"
            f"{'Corners':>20} {stats.get('corners_home', 0):>10}  {stats.get('corners_away', 0):>10}\n"
            f"{'Fouls':>20} {stats.get('fouls_home', 0):>10}  {stats.get('fouls_away', 0):>10}\n"
            f"{'Yellow Cards':>20} {stats.get('yellow_cards_home', 0):>10}  {stats.get('yellow_cards_away', 0):>10}\n"
            f"{'Red Cards':>20} {stats.get('red_cards_home', 0):>10}  {stats.get('red_cards_away', 0):>10}\n"
            f"{'─' * 42}\n"
            f"{'Total Corners':>20} {total_corners:>10}\n"
            f"```"
        )

    # ── Manual Command ───────────────────────────────

    @commands.command(name="stats")
    async def show_stats(self, ctx):
        """Show current match stats."""
        engine = self.bot.get_cog("MatchEngine")
        if not engine or not engine.state.is_live:
            await ctx.send(f"{config.STATMAN_PREFIX} Match is not live yet.")
            return
        self.bot.dispatch("match_stats_update", engine.state.stats.copy())

    @commands.command(name="fact")
    async def show_fact(self, ctx):
        """Drop a random diaspora fact."""
        fact = self._random_fact()
        if fact:
            await ctx.send(f"💡 **Did you know?** {fact}")
        else:
            await ctx.send("No facts loaded.")


async def setup(bot: commands.Bot):
    await bot.add_cog(StatManAgent(bot))
