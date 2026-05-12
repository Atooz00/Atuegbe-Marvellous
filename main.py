import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, BackgroundTasks
from telegram import Update
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.bot.handlers import start, help_command, balance, history, signals
from app.tasks.scheduler import setup_scheduler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "") # For production, e.g., https://your-domain.com/webhook

# Initialize Telegram App
ptb_app = None
if TELEGRAM_TOKEN:
    ptb_app = Application.builder().token(TELEGRAM_TOKEN).build()
    ptb_app.add_handler(CommandHandler("start", start))
    ptb_app.add_handler(CommandHandler("help", help_command))
    ptb_app.add_handler(CommandHandler("balance", balance))
    ptb_app.add_handler(CommandHandler("history", history))
    ptb_app.add_handler(CommandHandler("signals", signals))

# Setup APScheduler
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI application...")
    if ptb_app:
        await ptb_app.initialize()
        if WEBHOOK_URL:
            await ptb_app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
        else:
            await ptb_app.updater.start_polling()
            await ptb_app.start()

    # Start scheduler
    setup_scheduler(scheduler)
    scheduler.start()

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application...")
    scheduler.shutdown()
    if ptb_app:
        if not WEBHOOK_URL:
            await ptb_app.updater.stop()
        await ptb_app.stop()
        await ptb_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram updates by putting them into the update queue"""
    if not ptb_app:
        return {"status": "error", "message": "Bot not configured"}

    data = await request.json()
    update = Update.de_json(data, ptb_app.bot)

    # Run the bot logic in the background
    await ptb_app.process_update(update)

    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "TrenchOps API and Bot are running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
