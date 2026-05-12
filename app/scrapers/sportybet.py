import logging
import httpx
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def fetch_odds_for_market(match_id: int, market_name: str) -> Dict[str, Any]:
    """
    Mock scraping SportyBet internal JSON API for specific niche markets.
    In reality, this would use httpx to hit endpoints like /api/v1/markets/get_events
    and parse the complex JSON response.
    """
    logger.info(f"Mocking SportyBet scrape for match {match_id}, market: {market_name}")

    # We simulate different odds depending on the market to test the EV logic
    # The return format expects: {"implied_prob": float, "decimal_odds": float}

    mock_odds_db = {
        "Any Team Goal Streak 3+ (NO)": 1.05,
        "Corner Density (Under 13.5)": 1.15,
        "1st Half Bookings (Under 1.5)": 1.20,
        "Ten Minute Draw (00:00 - 09:59)": 1.12,
        "Penalty Awarded (NO)": 1.18,
        "First Goal Interval (1-15 Mins - NONE)": 1.25,
        "Home Multi Goals (1-3)": 1.08,
        "Away Multi Goals (0-3)": 1.04,
        "Either Team to Score in Both Halves (NO)": 1.10,
        "1st Half Goal Streak 2+ (NO)": 1.06
    }

    odds = mock_odds_db.get(market_name, 1.10)

    # Randomly fluctuate odds slightly to simulate live market movements
    import random
    fluctuation = random.uniform(-0.02, 0.02)
    final_odds = max(1.01, round(odds + fluctuation, 2))

    implied_prob = round(1 / final_odds, 4)

    return {
        "decimal_odds": final_odds,
        "implied_prob": implied_prob
    }
