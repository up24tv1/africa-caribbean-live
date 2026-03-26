"""
CAMERA — The Content Curator Agent
Captures best moments and packages them for sharing.
"""

import asyncio
import random
import discord
from discord.ext import commands
import config


class CameraAgent(commands.Cog):
    """Captures the best fan reactions and creates shareable content."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.goal_reactions = []  # Collected reactions after goals
        self.best_moments = []   # Top moments of the match

    def _channel(self):
        for guild in self.bot.guilds:
            for ch in guild.text_channels:
                if ch.name == config.CHANNELS["matchday"]:
                    return ch
        return None

    def _memes_channel(self):
        for guild in self.bot.guilds:
            for ch in guild.text_channels:
                if ch.name == config.CHANNELS["memes"]:
                    return ch
        return None

    # ── Goal Reaction Capture ────────────────────────

    @commands.Cog.listener()
    async def on_match_goal(self, team, scorer, minute, score_home, score_away):
        """After a goal, capture the best reactions for 60 seconds."""
        ch = self._channel()
        if not ch:
            return

        # Wait for reactions to pour in
        await asyncio.sleep(config.REACTION_CAPTURE_WINDOW)

        # Collect recent messages from the channel
        messages = []
        async for msg in ch.history(limit=50):
            if not msg.author.bot and msg.content:
                # Score = length of message + number of reactions on it
                score = len(msg.content) + sum(r.count for r in msg.reactions) * 3
                messages.append({
                    "author": msg.author.display_name,
                    "content": msg.content[:100],
                    "score": score,
                    "reactions": sum(r.count for r in msg.reactions),
                })

        # Sort by engagement score
        messages.sort(key=lambda x: x["score"], reverse=True)
        top = messages[:config.TOP_REACTIONS_COUNT]

        if top:
            self.best_moments.extend(top[:2])  # Save top 2 for recap

            lines = []
            for i, msg in enumerate(top):
                lines.append(
                    f"**{i+1}.** {msg['author']}: \"{msg['content']}\""
                    f" {'🔥' * min(msg['reactions'], 5)}"
                )

            await ch.send(
                f"# {config.CAMERA_PREFIX} GOAL REACTION CAM\n\n"
                f"**{scorer} ({team}) — {minute}'**\n\n"
                f"Top fan reactions:\n" +
                "\n".join(lines) +
                f"\n\n*Your reaction could be next! Keep the energy up.*"
            )

    # ── Halftime Highlights ──────────────────────────

    @commands.Cog.listener()
    async def on_match_halftime(self, score_home, score_away):
        memes_ch = self._memes_channel()
        if not memes_ch or not self.best_moments:
            return

        lines = []
        for i, moment in enumerate(self.best_moments[:5]):
            lines.append(f"**{i+1}.** {moment['author']}: \"{moment['content']}\"")

        await memes_ch.send(
            f"# {config.CAMERA_PREFIX} FIRST HALF HIGHLIGHTS\n\n"
            f"Best fan moments from the first 45:\n\n" +
            "\n".join(lines) +
            f"\n\n*Post your best memes here for the second half recap!*"
        )

    # ── Full Time Recap ──────────────────────────────

    @commands.Cog.listener()
    async def on_match_fulltime(self, score_home, score_away):
        ch = self._channel()
        memes_ch = self._memes_channel()
        target = memes_ch or ch
        if not target:
            return

        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM
        away = engine.state.away_team if engine else config.MATCH_AWAY_TEAM

        # Collect final best moments
        if ch:
            async for msg in ch.history(limit=100):
                if not msg.author.bot and msg.content and sum(r.count for r in msg.reactions) >= 2:
                    self.best_moments.append({
                        "author": msg.author.display_name,
                        "content": msg.content[:80],
                        "score": sum(r.count for r in msg.reactions),
                        "reactions": sum(r.count for r in msg.reactions),
                    })

        # Deduplicate and sort
        seen = set()
        unique = []
        for m in self.best_moments:
            key = f"{m['author']}:{m['content'][:30]}"
            if key not in seen:
                seen.add(key)
                unique.append(m)
        unique.sort(key=lambda x: x.get("score", 0), reverse=True)

        lines = []
        for i, moment in enumerate(unique[:8]):
            lines.append(f"**{i+1}.** {moment['author']}: \"{moment['content']}\"")

        await target.send(
            f"# {config.CAMERA_PREFIX} MATCH RECAP — BEST MOMENTS\n\n"
            f"## {home} {score_home} - {score_away} {away}\n\n"
            f"The Global Watch Room delivered. Here are the top fan moments:\n\n" +
            ("\n".join(lines) if lines else "*No reactions captured.*") +
            f"\n\n"
            f"**Share this match experience:**\n"
            f"Tag us and use the hashtag when posting your screenshots!\n\n"
            f"*See you at the next match. The stadium never closes.* 🌍⚽"
        )

    # ── Manual Snapshot ──────────────────────────────

    @commands.command(name="snapshot")
    @commands.has_permissions(manage_messages=True)
    async def take_snapshot(self, ctx):
        """Capture current top messages in the channel."""
        messages = []
        async for msg in ctx.channel.history(limit=30):
            if not msg.author.bot and msg.content:
                score = sum(r.count for r in msg.reactions)
                if score > 0:
                    messages.append({
                        "author": msg.author.display_name,
                        "content": msg.content[:80],
                        "reactions": score,
                    })

        messages.sort(key=lambda x: x["reactions"], reverse=True)
        top = messages[:5]

        if not top:
            await ctx.send(f"{config.CAMERA_PREFIX} No reactions to capture yet.")
            return

        lines = [f"**{i+1}.** {m['author']}: \"{m['content']}\" (🔥 {m['reactions']})"
                 for i, m in enumerate(top)]

        await ctx.send(
            f"# {config.CAMERA_PREFIX} SNAPSHOT\n\n" +
            "\n".join(lines)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CameraAgent(bot))
