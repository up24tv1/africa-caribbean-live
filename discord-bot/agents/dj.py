"""
DJ DIASPORA — The Soundtrack Agent
Curates the vibe with music links timed to match moments.
"""

import json
import os
import random
import discord
from discord.ext import commands
import config


PLAYLISTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "playlists.json")


class DJAgent(commands.Cog):
    """The stadium DJ — drops tracks timed to match events."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.playlists = self._load_playlists()
        self.goal_tracks_used = set()

    def _load_playlists(self):
        try:
            with open(PLAYLISTS_PATH, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "prematch": [],
                "goal_home": [],
                "goal_away": [],
                "halftime": [],
                "victory": [],
                "defeat": [],
                "hype": [],
            }

    def _channel(self):
        for guild in self.bot.guilds:
            for ch in guild.text_channels:
                if ch.name == config.CHANNELS["matchday"]:
                    return ch
        return None

    def _pick_track(self, category):
        tracks = self.playlists.get(category, [])
        if not tracks:
            return None
        available = [t for t in tracks if t.get("url") not in self.goal_tracks_used]
        if not available:
            self.goal_tracks_used.clear()
            available = tracks
        track = random.choice(available)
        self.goal_tracks_used.add(track.get("url"))
        return track

    # ── Pre-match ────────────────────────────────────

    @commands.Cog.listener()
    async def on_match_prematch(self, minutes: int):
        if minutes != 60:
            return

        ch = self._channel()
        if not ch:
            return

        track = self._pick_track("prematch")
        playlist_line = ""
        if track:
            playlist_line = f"\n🔗 **Now Playing:** [{track['title']}]({track['url']})"

        await ch.send(
            f"# {config.DJ_PREFIX} DJ DIASPORA IN THE BUILDING\n\n"
            f"The pre-match warmup is ON. Afrobeats meets Dancehall.\n\n"
            f"Get your speakers ready. The vibe starts NOW."
            f"{playlist_line}\n\n"
            f"*Request a track: `!request [song name]`*"
        )

    # ── Goal Celebration ─────────────────────────────

    @commands.Cog.listener()
    async def on_match_goal(self, team, scorer, minute, score_home, score_away):
        ch = self._channel()
        if not ch:
            return

        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM

        if team == home:
            track = self._pick_track("goal_home")
        else:
            track = self._pick_track("goal_away")

        if track:
            await ch.send(
                f"{config.DJ_PREFIX} **GOAL TRACK** 🔊\n"
                f"[{track['title']}]({track['url']})\n"
                f"*{track.get('vibe', 'Celebration mode!')}*"
            )

    # ── Halftime Mix ─────────────────────────────────

    @commands.Cog.listener()
    async def on_match_halftime(self, score_home, score_away):
        ch = self._channel()
        if not ch:
            return

        track = self._pick_track("halftime")
        track_line = f"\n🔗 [{track['title']}]({track['url']})" if track else ""

        await ch.send(
            f"# {config.DJ_PREFIX} HALFTIME MIX\n\n"
            f"Cooling down for 15 minutes. The DJ switches gears.\n"
            f"Smooth vibes while you catch your breath."
            f"{track_line}"
        )

    # ── Full Time ────────────────────────────────────

    @commands.Cog.listener()
    async def on_match_fulltime(self, score_home, score_away):
        ch = self._channel()
        if not ch:
            return

        if score_home > score_away:
            track = self._pick_track("victory")
            mood = "VICTORY ANTHEM"
        elif score_away > score_home:
            track = self._pick_track("defeat")
            mood = "Respect playlist"
        else:
            track = self._pick_track("hype")
            mood = "DRAW — both sides hold their heads high"

        track_line = f"\n🔗 [{track['title']}]({track['url']})" if track else ""

        await ch.send(
            f"# {config.DJ_PREFIX} POST-MATCH — {mood}\n\n"
            f"The final whistle has blown. The DJ keeps the energy alive."
            f"{track_line}\n\n"
            f"*Thanks for vibing with DJ Diaspora tonight. Until next time.* 🎧"
        )

    # ── Request Command ──────────────────────────────

    @commands.command(name="request")
    async def request_song(self, ctx, *, song: str):
        """Request a track from the DJ."""
        await ctx.send(
            f"{config.DJ_PREFIX} **Track requested:** {song}\n"
            f"DJ Diaspora has added it to the queue. 🎧"
        )

    @commands.command(name="playlist")
    async def show_playlist(self, ctx):
        """Show the current mood playlist."""
        engine = self.bot.get_cog("MatchEngine")
        if engine and engine.state.is_live:
            mood = "hype"
        elif engine and engine.state.status == "halftime":
            mood = "halftime"
        else:
            mood = "prematch"

        tracks = self.playlists.get(mood, [])[:5]
        if not tracks:
            await ctx.send(f"{config.DJ_PREFIX} No tracks loaded for this mood.")
            return

        lines = [f"- [{t['title']}]({t['url']})" for t in tracks]
        await ctx.send(
            f"# {config.DJ_PREFIX} Current Playlist — {mood.upper()}\n\n" +
            "\n".join(lines)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(DJAgent(bot))
