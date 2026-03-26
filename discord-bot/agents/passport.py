"""
PASSPORT CONTROL — The Onboarding Agent
Greets new members, assigns tribe/country roles, announces arrivals.
"""

import discord
from discord.ext import commands
import config


COUNTRY_FLAGS = {
    "jamaica": "🇯🇲", "dr congo": "🇨🇩", "congo": "🇨🇩",
    "nigeria": "🇳🇬", "ghana": "🇬🇭", "trinidad": "🇹🇹",
    "senegal": "🇸🇳", "haiti": "🇭🇹", "cameroon": "🇨🇲",
    "barbados": "🇧🇧", "dominican republic": "🇩🇴",
}

FLAG_TO_COUNTRY = {v: k.title() for k, v in COUNTRY_FLAGS.items()}

AFRICA_COUNTRIES = {"nigeria", "ghana", "senegal", "cameroon", "dr congo", "congo"}
CARIBBEAN_COUNTRIES = {"jamaica", "trinidad", "haiti", "barbados", "dominican republic"}


class PassportAgent(commands.Cog):
    """Handles member onboarding — role assignment and welcome announcements."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _get_channel(self, name_key):
        for guild in self.bot.guilds:
            for ch in guild.text_channels:
                if ch.name == config.CHANNELS.get(name_key, ""):
                    return ch
        return None

    async def _ensure_role(self, guild, role_name):
        """Get or create a role by name."""
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            try:
                role = await guild.create_role(name=role_name)
            except discord.errors.Forbidden:
                return None
        return role

    # ── New Member Join ──────────────────────────────

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_ch = self._get_channel("welcome")
        prove_ch = self._get_channel("prove_country")

        # DM the new member
        try:
            await member.send(
                f"# {config.PASSPORT_PREFIX} Welcome to Africa x Caribbean Live!\n\n"
                f"You just entered the **Global Watch Room** — the digital stadium for "
                f"the biggest diaspora matchup of the year.\n\n"
                f"**To get your passport stamp, head to #prove-your-country and tell us:**\n"
                f"1. What country are you repping?\n"
                f"2. What city are you watching from?\n\n"
                f"You can also reply here with a flag emoji (🇯🇲 🇨🇩 🇳🇬 etc.) "
                f"and I'll assign your role automatically!\n\n"
                f"See you in the stadium! ⚽"
            )
        except discord.errors.Forbidden:
            pass  # DMs disabled

        # Announce in welcome channel
        if welcome_ch:
            await welcome_ch.send(
                f"{config.PASSPORT_PREFIX} **{member.display_name}** just entered the stadium! "
                f"Head to #prove-your-country to get your passport stamp."
            )

    # ── Country Proving (message in #prove-your-country) ──

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        # Only process in #prove-your-country or DMs
        is_prove_channel = message.channel.name == config.CHANNELS.get("prove_country", "")
        is_dm = isinstance(message.channel, discord.DMChannel)

        if not is_prove_channel and not is_dm:
            return

        content_lower = message.content.lower().strip()
        guild = message.guild if message.guild else self.bot.guilds[0] if self.bot.guilds else None
        if not guild:
            return

        member = message.author
        if is_dm:
            member = guild.get_member(message.author.id)
            if not member:
                return

        # Check for flag emojis
        assigned_country = None
        for flag, country in FLAG_TO_COUNTRY.items():
            if flag in message.content:
                assigned_country = country
                break

        # Check for country names
        if not assigned_country:
            for country_name in COUNTRY_FLAGS:
                if country_name in content_lower:
                    assigned_country = country_name.title()
                    if assigned_country == "Congo":
                        assigned_country = "DR Congo"
                    break

        if not assigned_country:
            return  # No country detected, ignore

        # Assign country role
        country_role = await self._ensure_role(guild, assigned_country)
        if country_role:
            try:
                await member.add_roles(country_role)
            except discord.errors.Forbidden:
                pass

        # Assign team role (Africa or Caribbean)
        team_name = None
        if assigned_country.lower() in AFRICA_COUNTRIES:
            team_name = config.TEAM_ROLES["africa"]
        elif assigned_country.lower() in CARIBBEAN_COUNTRIES:
            team_name = config.TEAM_ROLES["caribbean"]

        if team_name:
            team_role = await self._ensure_role(guild, team_name)
            if team_role:
                try:
                    await member.add_roles(team_role)
                except discord.errors.Forbidden:
                    pass

        # Confirm
        flag = COUNTRY_FLAGS.get(assigned_country.lower(), "🌍")
        response_ch = message.channel if not is_dm else self._get_channel("prove_country")

        if response_ch:
            await response_ch.send(
                f"{config.PASSPORT_PREFIX} **PASSPORT STAMPED!** {flag}\n\n"
                f"**{member.display_name}** is repping **{assigned_country}**"
                f"{f' — {team_name}!' if team_name else '!'}\n\n"
                f"Welcome to your section of the stadium!"
            )

    # ── Manual Role Assignment ───────────────────────

    @commands.command(name="tribe")
    async def set_tribe(self, ctx, *, tribe: str):
        """Manually set your tribe: africa, caribbean, or neutral."""
        tribe_lower = tribe.lower().strip()
        if tribe_lower not in config.TEAM_ROLES:
            await ctx.send(
                f"Choose a tribe: `!tribe africa`, `!tribe caribbean`, or `!tribe neutral`"
            )
            return

        role_name = config.TEAM_ROLES[tribe_lower]
        role = await self._ensure_role(ctx.guild, role_name)
        if role:
            # Remove other tribe roles first
            for other_tribe in config.TEAM_ROLES.values():
                other_role = discord.utils.get(ctx.guild.roles, name=other_tribe)
                if other_role and other_role in ctx.author.roles:
                    await ctx.author.remove_roles(other_role)
            await ctx.author.add_roles(role)
            await ctx.send(
                f"{config.PASSPORT_PREFIX} {ctx.author.mention} — "
                f"You are now **{role_name}**! Welcome to your tribe."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(PassportAgent(bot))
