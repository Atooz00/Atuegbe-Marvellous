import logging
from app.database import supabase
from app.scrapers.rapidapi import fetch_match_stats

logger = logging.getLogger(__name__)

async def process_resulting():
    """
    Check finished matches, update stats, and settle bets.
    """
    if not supabase:
        logger.warning("Supabase not configured, skipping resulting engine")
        return

    logger.info("Running Resulting Engine...")

    try:
        # Get pending bets
        pending_bets = supabase.table("bet_ledger").select("*").eq("status", "pending").execute()

        if not pending_bets.data:
            logger.info("No pending bets to settle.")
            return

        for bet in pending_bets.data:
            # We don't have a direct link from bet to match_id in the current simple ledger schema,
            # so for demonstration purposes we will just fetch a mock match ID.
            # In production, bet_ledger would have a match_id or selection_id pointing to the match.
            mock_match_id = 12345

            # 1. Fetch match stats from API
            stats = await fetch_match_stats(mock_match_id)

            # 2. Update match_stats table
            # Check if stats already exist for this match
            existing_stats = supabase.table("match_stats").select("*").eq("match_id", mock_match_id).execute()
            stats_data = {
                "match_id": mock_match_id,
                "home_corners": stats.get("home_corners", 0),
                "away_corners": stats.get("away_corners", 0),
                "home_yellow_cards_ht": stats.get("home_yellow_cards_ht", 0),
                "away_yellow_cards_ht": stats.get("away_yellow_cards_ht", 0),
                "penalty_awarded": stats.get("penalty_awarded", False)
            }
            if existing_stats.data:
                supabase.table("match_stats").update(stats_data).eq("match_id", mock_match_id).execute()
            else:
                supabase.table("match_stats").insert(stats_data).execute()

            # 3. Update goal_events table
            for goal in stats.get("goals", []):
                # We check if a similar goal exists to avoid duplicates (mock logic)
                supabase.table("goal_events").upsert({
                    "match_id": mock_match_id,
                    "scoring_team": goal["team"],
                    "minute": goal["minute"],
                    "half": goal["half"]
                }, on_conflict="id").execute() # In production we would need a proper unique constraint for upsert

            # 4. Settle Bet logic based on the stats
            # For this mock, we will evaluate some basic logic based on market name
            market = bet['market']
            is_win = False

            if "Corner Density (Under 13.5)" in market:
                is_win = (stats.get("home_corners", 0) + stats.get("away_corners", 0)) < 13.5
            elif "Penalty Awarded (NO)" in market:
                is_win = not stats.get("penalty_awarded", False)
            elif "Home Multi Goals" in market:
                home_goals = len([g for g in stats.get("goals", []) if g["team"] == "home"])
                is_win = 1 <= home_goals <= 3
            else:
                # Default mock resolution for other markets
                import random
                is_win = random.random() < 0.60

            result = "WIN" if is_win else "LOSS"
            status = "settled"

            # Update ledger
            supabase.table("bet_ledger").update(
                {"status": status, "result": result}
            ).eq("id", bet['id']).execute()

            # Update user balance
            user_data = supabase.table("user_profiles").select("current_balance").eq("id", bet['user_id']).execute()
            if user_data.data:
                current_balance = user_data.data[0]['current_balance']

                # Mock stake amount (e.g., $10)
                stake = 10.0

                if is_win:
                    profit = stake * (bet['odds'] - 1)
                    new_balance = current_balance + profit
                else:
                    new_balance = current_balance - stake

                supabase.table("user_profiles").update(
                    {"current_balance": new_balance}
                ).eq("id", bet['user_id']).execute()

                logger.info(f"Settled bet {bet['id']} for user {bet['user_id']}: {result} (Market: {market})")

    except Exception as e:
        logger.error(f"Error in resulting engine: {e}")
