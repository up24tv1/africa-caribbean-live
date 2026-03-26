"""
HYPE — The MC / Host Agent
Main energy driver. Opens the event, hypes the crowd, calls the action.
"""

import random
import discord
from discord.ext import commands
import config


class HypeAgent(commands.Cog):
    """The stadium MC — drives energy and narrates the match."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _channel(self):
        for guild in self.bot.guilds:
            for ch in guild.text_channels:
                if ch.name == config.CHANNELS["matchday"]:
                    return ch
        return None

    # ── Pre-match Countdown ──────────────────────────

    @commands.Cog.listener()
    async def on_match_prematch(self, minutes: int):
        ch = self._channel()
        if not ch:
            return

        messages = {
            60: (
                f"# {config.HYPE_PREFIX} 1 HOUR TO KICKOFF\n\n"
                f"**{config.MATCH_HOME_TEAM} vs {config.MATCH_AWAY_TEAM}**\n\n"
                "The stadium doors are OPEN. Get in your voice rooms. "
                "Drop your predictions in #predictions. Rep your flag in #prove-your-country.\n\n"
                "**THIS IS NOT A DRILL.**"
            ),
            30: (
                f"# {config.HYPE_PREFIX} 30 MINUTES\n\n"
                "Half hour to kickoff. The energy is BUILDING.\n\n"
                "Voice rooms are filling up. If you're not in one yet, what are you doing?\n\n"
                f"**{config.MATCH_HOME_TEAM} vs {config.MATCH_AWAY_TEAM} — TONIGHT.**"
            ),
            15: (
                f"# {config.HYPE_PREFIX} 15 MINUTES\n\n"
                "Players are in the tunnel. The anthem is about to play.\n\n"
                "**LAST CALL for predictions.** Lock them in NOW.\n\n"
                "This stadium is ELECTRIC."
            ),
            5: (
                f"# {config.HYPE_PREFIX} 5 MINUTES\n\n"
                "🚨 **FIVE MINUTES** 🚨\n\n"
                "The referee is checking his watch. "
                "The stadium is ROARING. Your voice room is your section.\n\n"
                "**BUCKLE UP.**"
            ),
            1: (
                f"# {config.HYPE_PREFIX} ONE MINUTE\n\n"
                "⚡ **60 SECONDS TO KICKOFF** ⚡\n\n"
                "Everyone on your feet. THIS IS IT."
            ),
        }

        msg = messages.get(minutes)
        if msg:
            await ch.send(msg)

    # ── Kickoff ──────────────────────────────────────

    @commands.Cog.listener()
    async def on_match_kickoff(self):
        ch = self._channel()
        if not ch:
            return

        await ch.send(
            f"# ⚽ KICKOFF! ⚽\n\n"
            f"**{config.MATCH_HOME_TEAM} vs {config.MATCH_AWAY_TEAM}**\n\n"
            f"The referee blows the whistle — WE ARE LIVE!\n\n"
            f"React in this channel. Jump in voice. THE GLOBAL STADIUM IS OPEN.\n\n"
            f"**LET'S GOOOOO!**"
        )

    # ── Goal ─────────────────────────────────────────

    @commands.Cog.listener()
    async def on_match_goal(self, team, scorer, minute, score_home, score_away):
        ch = self._channel()
        if not ch:
            return

        celebrations = [
            "THE STADIUM ERUPTS!",
            "ABSOLUTE SCENES!",
            "THE CROWD GOES WILD!",
            "CAN YOU BELIEVE IT?!",
            "WHAT A MOMENT!",
            "THE ROOF IS OFF THIS PLACE!",
        ]

        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM
        away = engine.state.away_team if engine else config.MATCH_AWAY_TEAM

        await ch.send(
            f"# ⚽⚽⚽ GOOOOOAAALLL! ⚽⚽⚽\n\n"
            f"**{scorer}** ({team}) — {minute}'\n\n"
            f"## {home} {score_home} - {score_away} {away}\n\n"
            f"**{random.choice(celebrations)}**"
        )

    # ── Card ─────────────────────────────────────────

    @commands.Cog.listener()
    async def on_match_card(self, team, player, card_type, minute):
        ch = self._channel()
        if not ch:
            return

        emoji = "🟨" if card_type == "yellow" else "🟥"
        severity = "Yellow card" if card_type == "yellow" else "RED CARD!"

        await ch.send(
            f"{emoji} **{severity}** — {player} ({team}) at {minute}'\n"
            f"{'The referee reaches for his pocket...' if card_type == 'yellow' else 'HE IS OFF! Drama in the stadium!'}"
        )

    # ── Halftime ─────────────────────────────────────

    @commands.Cog.listener()
    async def on_match_halftime(self, score_home, score_away):
        ch = self._channel()
        if not ch:
            return

        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM
        away = engine.state.away_team if engine else config.MATCH_AWAY_TEAM

        await ch.send(
            f"# ⏸️ HALFTIME\n\n"
            f"## {home} {score_home} - {score_away} {away}\n\n"
            f"45 minutes in the books. Time to catch your breath.\n\n"
            f"**Halftime activities starting NOW:**\n"
            f"- 🔮 Check your predictions in #predictions\n"
            f"- 🎵 DJ dropping the halftime mix\n"
            f"- 💬 Best takes go on stage — share your hot take!\n\n"
            f"**Second half in 15 minutes.**"
        )

    # ── Second Half ──────────────────────────────────

    @commands.Cog.listener()
    async def on_match_second_half(self):
        ch = self._channel()
        if not ch:
            return

        await ch.send(
            f"# ⚽ SECOND HALF — WE'RE BACK!\n\n"
            f"The whistle blows. 45 more minutes to settle this.\n\n"
            f"**EVERYTHING IS ON THE LINE.**"
        )

    # ── Full Time ────────────────────────────────────

    @commands.Cog.listener()
    async def on_match_fulltime(self, score_home, score_away):
        ch = self._channel()
        if not ch:
            return

        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM
        away = engine.state.away_team if engine else config.MATCH_AWAY_TEAM

        if score_home > score_away:
            result = f"**{home} WIN!**"
        elif score_away > score_home:
            result = f"**{away} WIN!**"
        else:
            result = "**IT'S A DRAW!**"

        await ch.send(
            f"# 🏁 FULL TIME 🏁\n\n"
            f"## {home} {score_home} - {score_away} {away}\n\n"
            f"{result}\n\n"
            f"What. A. Match.\n\n"
            f"**Post-match locker room is OPEN.**\n"
            f"- 🔮 Prediction results coming in #predictions\n"
            f"- 📸 Best moments recap dropping soon\n"
            f"- 💬 Share your reactions, memes, takes\n\n"
            f"**Thank you for being part of the Global Watch Room. "
            f"This was HISTORY.**"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(HypeAgent(bot))
