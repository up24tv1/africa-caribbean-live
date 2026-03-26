"""
Africa x Caribbean Live — AI Stadium Crew
Main bot entry point. Loads all 7 agents + Match Engine.

Usage:
  python -X utf8 bot.py              # Run with live/simulate mode
  python -X utf8 bot.py --simulate   # Force simulation mode
"""

import sys
import os
import asyncio
import discord
from discord.ext import commands

# Add parent to path for config
sys.path.insert(0, os.path.dirname(__file__))
import config

# ── Bot Setup ────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=commands.DefaultHelpCommand(no_category="General"),
)

# ── Cog Loading ──────────────────────────────────────

COGS = [
    "match_engine",
    "agents.hype",
    "agents.bouncer",
    "agents.passport",
    "agents.oracle",
    "agents.statman",
    "agents.dj",
    "agents.camera",
]


@bot.event
async def on_ready():
    print(f"\n{'='*50}")
    print(f"  AFRICA x CARIBBEAN LIVE — AI STADIUM CREW")
    print(f"{'='*50}")
    print(f"  Bot:    {bot.user}")
    print(f"  Guilds: {len(bot.guilds)}")
    for guild in bot.guilds:
        print(f"  Server: {guild.name} (ID: {guild.id})")
        print(f"  Members: {guild.member_count}")
    print(f"  Mode:   {config.MATCH_API_MODE}")
    print(f"{'='*50}")
    print(f"  Agents loaded:")
    for cog_name in bot.cogs:
        print(f"    ✓ {cog_name}")
    print(f"{'='*50}")
    print(f"  Commands: {', '.join(f'!{c.name}' for c in bot.commands)}")
    print(f"{'='*50}\n")


@bot.command(name="crew")
async def show_crew(ctx):
    """Show all active AI agents."""
    agents = {
        "MatchEngine": ("⚙️", "Match data engine — polls live data or simulates"),
        "HypeAgent": ("🔥", "HYPE — MC/Host, narrates the match"),
        "BouncerAgent": ("🛡️", "BOUNCER — Moderator, spam filter, warnings"),
        "PassportAgent": ("🛂", "PASSPORT — Onboarding, role assignment"),
        "OracleAgent": ("🔮", "ORACLE — Prediction games, leaderboard"),
        "StatManAgent": ("📊", "STAT MAN — Live stats, fun facts"),
        "DJAgent": ("🎵", "DJ DIASPORA — Soundtrack, playlists"),
        "CameraAgent": ("📸", "CAMERA — Reaction capture, recaps"),
    }

    lines = []
    for cog_name, (emoji, desc) in agents.items():
        status = "🟢 Online" if cog_name in bot.cogs else "🔴 Offline"
        lines.append(f"{emoji} **{cog_name}** — {desc} [{status}]")

    engine = bot.get_cog("MatchEngine")
    match_status = "Pre-match"
    if engine:
        match_status = engine.state.status.replace("_", " ").title()

    await ctx.send(
        f"# ⚽ AI STADIUM CREW — Status\n\n"
        f"**Match:** {config.MATCH_HOME_TEAM} vs {config.MATCH_AWAY_TEAM}\n"
        f"**Status:** {match_status}\n"
        f"**Mode:** {config.MATCH_API_MODE}\n\n" +
        "\n".join(lines) +
        f"\n\n*Use `!help` for all commands.*"
    )


@bot.command(name="status")
async def match_status(ctx):
    """Show current match status."""
    engine = bot.get_cog("MatchEngine")
    if not engine:
        await ctx.send("Match engine not loaded.")
        return

    s = engine.state
    await ctx.send(
        f"**{s.home_team} {s.score_home} - {s.score_away} {s.away_team}**\n"
        f"Status: {s.status} | Minute: {s.minute}'\n"
        f"Mode: {config.MATCH_API_MODE}"
    )


# ── Main ─────────────────────────────────────────────

async def main():
    # Parse CLI args
    if "--simulate" in sys.argv:
        config.MATCH_API_MODE = "simulate"

    # Load all cogs
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"  [+] Loaded: {cog}")
        except Exception as e:
            print(f"  [!] Failed to load {cog}: {e}")

    # Start bot
    token = config.BOT_TOKEN
    if not token:
        print("\n[ERROR] DISCORD_BOT_TOKEN not set!")
        print("Set it in your environment or .env file:")
        print("  export DISCORD_BOT_TOKEN=your_token_here")
        print("\nTo create a bot token:")
        print("  1. Go to https://discord.com/developers/applications")
        print("  2. Create New Application → Bot → Reset Token → Copy")
        print("  3. Enable: Message Content Intent, Server Members Intent")
        print("  4. Invite bot to your server with admin permissions")
        return

    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
