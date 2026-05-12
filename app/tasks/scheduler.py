import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks.resulting_engine import process_resulting
from app.scrapers.rapidapi import fetch_fixtures_by_date
from app.scrapers.sportybet import fetch_odds_for_market
from app.evaluators.modules import ALL_EVALUATORS
from datetime import datetime

logger = logging.getLogger(__name__)

async def run_market_scanners():
    """
    Mock task that runs through matches, scrapes odds, and evaluates signals.
    """
    logger.info("Running Market Scanners...")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 1. Fetch matches
    matches = await fetch_fixtures_by_date(today_str)

    for match in matches:
        match_id = match['match_id']
        logger.info(f"Scanning match {match_id} ({match['home_team']} vs {match['away_team']})")

        # 2. Evaluate each market
        for evaluator in ALL_EVALUATORS:
            # 3. Scrape odds
            odds_data = await fetch_odds_for_market(match_id, evaluator.market_name)

            # 4. Evaluate
            is_signal, signal_data = await evaluator.evaluate_signal(match_id, odds_data['decimal_odds'])

            if is_signal:
                logger.info(f"🚨 SIGNAL FOUND: {signal_data}")
                # In full production, this would broadcast via Telegram bot to users with signals_active=True

def setup_scheduler(scheduler: AsyncIOScheduler):
    """
    Add jobs to the scheduler.
    """
    # Run scanners every 5 minutes
    scheduler.add_job(run_market_scanners, 'interval', minutes=5, id='market_scanner')

    # Run resulting engine every 15 minutes
    scheduler.add_job(process_resulting, 'interval', minutes=15, id='resulting_engine')

    logger.info("Scheduler configured with tasks.")
