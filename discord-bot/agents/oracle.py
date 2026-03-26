"""
ORACLE — The Predictions Master Agent
Runs prediction games, tracks scores, announces winners.
"""

import json
import os
import discord
from discord.ext import commands
import config


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "predictions.json")


class OracleAgent(commands.Cog):
    """Prediction game master — manages predictions and leaderboard."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.predictions = self._load()
        self.locked = False

    def _load(self):
        try:
            with open(DB_PATH, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, "w") as f:
            json.dump(self.predictions, f, indent=2)

    def _channel(self):
        for guild in self.bot.guilds:
            for ch in guild.text_channels:
                if ch.name == config.CHANNELS["predictions"]:
                    return ch
        return None

    # ── Prediction Commands ──────────────────────────

    @commands.command(name="predict")
    async def predict(self, ctx, category: str, *, value: str):
        """
        Make a prediction.
        Usage:
          !predict score 2-1
          !predict scorer Bailey
          !predict motm Antonio
          !predict corners over
        """
        if self.locked:
            await ctx.send(f"{config.ORACLE_PREFIX} Predictions are **LOCKED**. The match has started!")
            return

        valid_categories = {
            "score": "final_score",
            "scorer": "first_scorer",
            "motm": "motm",
            "corners": "total_corners",
        }

        cat_key = valid_categories.get(category.lower())
        if not cat_key:
            await ctx.send(
                f"{config.ORACLE_PREFIX} Invalid category. Use: "
                f"`score`, `scorer`, `motm`, or `corners`"
            )
            return

        user_id = str(ctx.author.id)
        if user_id not in self.predictions:
            self.predictions[user_id] = {
                "name": ctx.author.display_name,
                "predictions": {},
                "points": 0,
            }

        self.predictions[user_id]["predictions"][cat_key] = value.strip()
        self._save()

        category_labels = {
            "final_score": "Final Score",
            "first_scorer": "First Goal Scorer",
            "motm": "Man of the Match",
            "total_corners": "Total Corners (over/under 9.5)",
        }

        await ctx.send(
            f"{config.ORACLE_PREFIX} **Prediction locked!**\n"
            f"**{ctx.author.display_name}** predicts "
            f"**{category_labels[cat_key]}**: {value}\n\n"
            f"Use `!mypredictions` to see all your picks."
        )

    @commands.command(name="mypredictions")
    async def my_predictions(self, ctx):
        """View your predictions."""
        user_id = str(ctx.author.id)
        if user_id not in self.predictions or not self.predictions[user_id]["predictions"]:
            await ctx.send(f"{config.ORACLE_PREFIX} You haven't made any predictions yet! Use `!predict`")
            return

        preds = self.predictions[user_id]["predictions"]
        lines = []
        labels = {
            "final_score": "Score",
            "first_scorer": "First Scorer",
            "motm": "MOTM",
            "total_corners": "Corners",
        }
        for key, label in labels.items():
            val = preds.get(key, "—")
            lines.append(f"- **{label}:** {val}")

        await ctx.send(
            f"{config.ORACLE_PREFIX} **{ctx.author.display_name}'s Predictions:**\n" +
            "\n".join(lines) +
            f"\n\nPoints: **{self.predictions[user_id]['points']}**"
        )

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx):
        """Show prediction leaderboard."""
        if not self.predictions:
            await ctx.send(f"{config.ORACLE_PREFIX} No predictions yet!")
            return

        sorted_users = sorted(
            self.predictions.values(),
            key=lambda x: x["points"],
            reverse=True
        )[:10]

        lines = []
        medals = ["🥇", "🥈", "🥉"]
        for i, user in enumerate(sorted_users):
            prefix = medals[i] if i < 3 else f"{i+1}."
            lines.append(f"{prefix} **{user['name']}** — {user['points']} pts")

        await ctx.send(
            f"# {config.ORACLE_PREFIX} Prediction Leaderboard\n\n" +
            "\n".join(lines) if lines else "No predictions yet."
        )

    # ── Match Event Listeners ────────────────────────

    @commands.Cog.listener()
    async def on_match_kickoff(self):
        """Lock predictions at kickoff."""
        self.locked = True
        ch = self._channel()
        if ch:
            count = len(self.predictions)
            await ch.send(
                f"# {config.ORACLE_PREFIX} PREDICTIONS LOCKED! 🔒\n\n"
                f"**{count} fans** have locked in their picks.\n\n"
                f"No more changes. Let's see who called it right!\n\n"
                f"Use `!leaderboard` to track the standings."
            )

    @commands.Cog.listener()
    async def on_match_goal(self, team, scorer, minute, score_home, score_away):
        """Score first-scorer predictions."""
        ch = self._channel()
        winners = []

        for user_id, data in self.predictions.items():
            pred = data["predictions"].get("first_scorer", "").lower()
            # Only score the FIRST goal
            if (score_home + score_away) == 1 and pred:
                if scorer.lower() in pred or pred in scorer.lower():
                    data["points"] += 3
                    winners.append(data["name"])

        self._save()

        if winners and ch:
            await ch.send(
                f"{config.ORACLE_PREFIX} **First Scorer: {scorer}!**\n\n"
                f"🎯 Correctly predicted by: **{', '.join(winners)}** (+3 pts each)"
            )

    @commands.Cog.listener()
    async def on_match_halftime(self, score_home, score_away):
        """Post halftime leaderboard."""
        ch = self._channel()
        if not ch:
            return

        sorted_users = sorted(
            self.predictions.values(),
            key=lambda x: x["points"],
            reverse=True
        )[:5]

        lines = []
        for i, user in enumerate(sorted_users):
            lines.append(f"{i+1}. **{user['name']}** — {user['points']} pts")

        await ch.send(
            f"# {config.ORACLE_PREFIX} Halftime Standings\n\n" +
            ("\n".join(lines) if lines else "No scores yet.") +
            f"\n\n**Second half predictions still in play!**"
        )

    @commands.Cog.listener()
    async def on_match_fulltime(self, score_home, score_away):
        """Score all remaining predictions and announce final results."""
        ch = self._channel()
        engine = self.bot.get_cog("MatchEngine")
        home = engine.state.home_team if engine else config.MATCH_HOME_TEAM
        away = engine.state.away_team if engine else config.MATCH_AWAY_TEAM
        final_score = f"{score_home}-{score_away}"
        total_corners = (engine.state.stats.get("corners_home", 0) +
                        engine.state.stats.get("corners_away", 0)) if engine else 0

        for user_id, data in self.predictions.items():
            preds = data["predictions"]

            # Score prediction
            pred_score = preds.get("final_score", "").replace(" ", "")
            if pred_score == final_score:
                data["points"] += 5
            elif pred_score:
                # Check if they got the winner right
                try:
                    ph, pa = pred_score.split("-")
                    if (int(ph) > int(pa)) == (score_home > score_away):
                        data["points"] += 1
                except (ValueError, IndexError):
                    pass

            # Corners prediction
            pred_corners = preds.get("total_corners", "").lower()
            if pred_corners == "over" and total_corners > 9:
                data["points"] += 2
            elif pred_corners == "under" and total_corners <= 9:
                data["points"] += 2

        self._save()

        # Announce winners
        if ch:
            sorted_users = sorted(
                self.predictions.values(),
                key=lambda x: x["points"],
                reverse=True
            )[:10]

            lines = []
            medals = ["🥇", "🥈", "🥉"]
            for i, user in enumerate(sorted_users):
                prefix = medals[i] if i < 3 else f"{i+1}."
                lines.append(f"{prefix} **{user['name']}** — {user['points']} pts")

            winner = sorted_users[0]["name"] if sorted_users else "No one"

            await ch.send(
                f"# {config.ORACLE_PREFIX} FINAL PREDICTION RESULTS 🏆\n\n"
                f"**Final Score:** {home} {final_score.replace('-', ' - ')} {away}\n"
                f"**Total Corners:** {total_corners}\n\n"
                f"## Leaderboard\n\n" +
                "\n".join(lines) +
                f"\n\n🏆 **{winner} is the Oracle Champion!**"
            )

    # ── Admin ────────────────────────────────────────

    @commands.command(name="unlock_predictions")
    @commands.has_permissions(administrator=True)
    async def unlock_predictions(self, ctx):
        self.locked = False
        await ctx.send(f"{config.ORACLE_PREFIX} Predictions UNLOCKED.")

    @commands.command(name="reset_predictions")
    @commands.has_permissions(administrator=True)
    async def reset_predictions(self, ctx):
        self.predictions = {}
        self._save()
        await ctx.send(f"{config.ORACLE_PREFIX} All predictions cleared.")


async def setup(bot: commands.Bot):
    await bot.add_cog(OracleAgent(bot))
