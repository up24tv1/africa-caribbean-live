"""
Configuration for Africa x Caribbean Live Discord Bot.
All 7 AI agents + Match Engine settings.
"""

import os

# ── Bot ──────────────────────────────────────────────
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "1486504785439100991"))

# ── Channel Names (auto-resolved to IDs at startup) ──
CHANNELS = {
    "general": "general",
    "welcome": "welcome",
    "matchday": "matchday-live",
    "predictions": "predictions",
    "prove_country": "prove-your-country",
    "memes": "memes-and-banter",
}

# ── Match Engine ─────────────────────────────────────
# Using free API-Football via RapidAPI, or set to "simulate" for demo mode
MATCH_API_MODE = os.getenv("MATCH_API_MODE", "simulate")  # "live" or "simulate"
MATCH_API_KEY = os.getenv("MATCH_API_KEY", "")
MATCH_API_HOST = "api-football-v1.p.rapidapi.com"

# Match details
MATCH_HOME_TEAM = "Jamaica"
MATCH_AWAY_TEAM = "New Caledonia"
MATCH_DATE = "2026-03-26"
MATCH_TIME_UTC = "20:00"
MATCH_FIXTURE_ID = None  # Set when found via API, or leave None for simulate

# Poll interval in seconds
MATCH_POLL_INTERVAL = 30

# ── Agent: HYPE (MC/Host) ────────────────────────────
HYPE_PREFIX = "🔥"
COUNTDOWN_INTERVALS = [60, 30, 15, 5, 1]  # minutes before kickoff

# ── Agent: DJ DIASPORA ───────────────────────────────
DJ_PREFIX = "🎵"

# ── Agent: ORACLE (Predictions) ──────────────────────
ORACLE_PREFIX = "🔮"
PREDICTION_LOCK_AT_KICKOFF = True
PREDICTION_CATEGORIES = [
    "final_score",
    "first_scorer",
    "motm",         # man of the match
    "total_corners", # over/under 9.5
]

# ── Agent: PASSPORT CONTROL ─────────────────────────
PASSPORT_PREFIX = "🛂"
TEAM_ROLES = {
    "africa": "Team Africa",
    "caribbean": "Team Caribbean",
    "neutral": "Neutral Fan",
}
COUNTRY_ROLES = [
    "Jamaica", "DR Congo", "Nigeria", "Ghana",
    "Trinidad", "Senegal", "Haiti", "Cameroon",
    "Barbados", "Dominican Republic",
]
STRIPE_TIER_ROLES = ["Supporter", "Super Fan", "Fam", "Captain"]

# ── Agent: BOUNCER (Moderator) ───────────────────────
BOUNCER_PREFIX = "🛡️"
SPAM_RATE_LIMIT = 5          # max messages per 5 seconds
MUTE_DURATIONS = [300, 1800]  # 5 min, 30 min (seconds)
BANNED_WORDS_FILE = "data/banned_words.json"

# ── Agent: STAT MAN ──────────────────────────────────
STATMAN_PREFIX = "📊"
STATS_INTERVAL_MINUTES = 15

# ── Agent: CAMERA ────────────────────────────────────
CAMERA_PREFIX = "📸"
REACTION_CAPTURE_WINDOW = 60  # seconds after goal to capture reactions
TOP_REACTIONS_COUNT = 5
