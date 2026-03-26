"""
BOUNCER — The Moderator Agent
Keeps the stadium safe. Auto-moderation, spam prevention, escalating warnings.
"""

import json
import os
import time
from collections import defaultdict
import discord
from discord.ext import commands
import config


class BouncerAgent(commands.Cog):
    """Automated moderator — spam filter, banned words, rate limiting."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_messages = defaultdict(list)  # user_id -> [timestamps]
        self.warnings = defaultdict(int)         # user_id -> warning count
        self.muted_until = {}                    # user_id -> unmute timestamp
        self.banned_words = self._load_banned_words()

    def _load_banned_words(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config.BANNED_WORDS_FILE)
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _get_mod_log(self, guild):
        for ch in guild.text_channels:
            if ch.name == "mod-log":
                return ch
        return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Check if user is muted
        if message.author.id in self.muted_until:
            if time.time() < self.muted_until[message.author.id]:
                try:
                    await message.delete()
                except discord.errors.Forbidden:
                    pass
                return
            else:
                del self.muted_until[message.author.id]

        # ── Banned Words Check ───────────────────────
        content_lower = message.content.lower()
        for word in self.banned_words:
            if word.lower() in content_lower:
                try:
                    await message.delete()
                except discord.errors.Forbidden:
                    pass
                self.warnings[message.author.id] += 1
                await self._handle_warning(message)
                return

        # ── Illegal Stream Links ─────────────────────
        stream_keywords = ["stream2watch", "crackstreams", "buffstream",
                          "soccerstreams", "hesgoal", "totalsportek"]
        for kw in stream_keywords:
            if kw in content_lower:
                try:
                    await message.delete()
                except discord.errors.Forbidden:
                    pass
                await message.channel.send(
                    f"{config.BOUNCER_PREFIX} {message.author.mention} — "
                    f"No illegal stream links. Use your local broadcaster (FIFA+, DStv, SportsMax).",
                    delete_after=10
                )
                return

        # ── Rate Limiting ────────────────────────────
        now = time.time()
        user_id = message.author.id
        self.user_messages[user_id] = [
            t for t in self.user_messages[user_id] if now - t < 5
        ]
        self.user_messages[user_id].append(now)

        if len(self.user_messages[user_id]) > config.SPAM_RATE_LIMIT:
            try:
                await message.delete()
            except discord.errors.Forbidden:
                pass
            self.warnings[user_id] += 1
            await message.channel.send(
                f"{config.BOUNCER_PREFIX} {message.author.mention} — "
                f"Slow down! You're sending messages too fast.",
                delete_after=5
            )
            await self._handle_warning(message)

    async def _handle_warning(self, message: discord.Message):
        user_id = message.author.id
        count = self.warnings[user_id]
        mod_log = self._get_mod_log(message.guild)

        if count == 1:
            await message.channel.send(
                f"{config.BOUNCER_PREFIX} {message.author.mention} — "
                f"**Warning 1/3.** Keep it clean.",
                delete_after=10
            )
        elif count == 2:
            # Mute for 5 minutes
            duration = config.MUTE_DURATIONS[0]
            self.muted_until[user_id] = time.time() + duration
            await message.channel.send(
                f"{config.BOUNCER_PREFIX} {message.author.mention} — "
                f"**Warning 2/3.** Muted for 5 minutes.",
                delete_after=10
            )
            if mod_log:
                await mod_log.send(
                    f"🔇 **Muted** {message.author} for 5 min. "
                    f"Reason: {count} warnings. Channel: #{message.channel.name}"
                )
        elif count >= 3:
            # Mute for 30 minutes
            duration = config.MUTE_DURATIONS[1]
            self.muted_until[user_id] = time.time() + duration
            await message.channel.send(
                f"{config.BOUNCER_PREFIX} {message.author.mention} — "
                f"**Warning 3/3.** Muted for 30 minutes. Next offense = kick.",
                delete_after=10
            )
            if mod_log:
                await mod_log.send(
                    f"🔇 **Muted** {message.author} for 30 min. "
                    f"Reason: {count} warnings. Channel: #{message.channel.name}"
                )

    # ── Goal Spam Prevention ─────────────────────────

    @commands.Cog.listener()
    async def on_match_goal(self, team, scorer, minute, score_home, score_away):
        """Temporarily increase rate limit tolerance after goals."""
        # Allow more messages for 30 seconds after a goal
        original_limit = config.SPAM_RATE_LIMIT
        config.SPAM_RATE_LIMIT = 15
        await discord.utils.sleep_until(
            discord.utils.utcnow() + __import__("datetime").timedelta(seconds=30)
        )
        config.SPAM_RATE_LIMIT = original_limit

    # ── Admin Commands ───────────────────────────────

    @commands.command(name="unmute")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmute a user."""
        if member.id in self.muted_until:
            del self.muted_until[member.id]
            self.warnings[member.id] = 0
            await ctx.send(f"{config.BOUNCER_PREFIX} {member.mention} has been unmuted.")
        else:
            await ctx.send(f"{member.mention} is not muted.")

    @commands.command(name="clearwarnings")
    @commands.has_permissions(manage_messages=True)
    async def clear_warnings(self, ctx, member: discord.Member):
        """Clear warnings for a user."""
        self.warnings[member.id] = 0
        await ctx.send(f"{config.BOUNCER_PREFIX} Warnings cleared for {member.mention}.")


async def setup(bot: commands.Bot):
    await bot.add_cog(BouncerAgent(bot))
