from telegram import Update
from telegram.ext import ContextTypes
from app.database import supabase
import logging

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    if user and supabase:
        try:
            # Upsert user
            data = supabase.table("user_profiles").upsert(
                {
                    "telegram_id": user.id,
                    "current_balance": 1000.00,  # Default virtual capital
                    "kelly_multiplier": 0.25,
                    "signals_active": True
                },
                on_conflict="telegram_id"
            ).execute()
        except Exception as e:
            logger.error(f"Error creating user profile: {e}")

    await update.message.reply_html(
        f"Welcome {user.mention_html()} to TrenchOps Bot! 🚀\n"
        "Type /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "/start - Start the bot\n"
        "/balance - Check your virtual balance\n"
        "/history - View your bet history\n"
        "/signals - Toggle live notifications"
    )
    await update.message.reply_text(help_text)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the user's virtual balance."""
    user = update.effective_user
    if not supabase:
        await update.message.reply_text("Database not connected.")
        return

    try:
        response = supabase.table("user_profiles").select("current_balance").eq("telegram_id", user.id).execute()
        if response.data:
            bal = response.data[0]['current_balance']
            await update.message.reply_text(f"Your current virtual balance is: ${bal:.2f}")
        else:
            await update.message.reply_text("Please run /start first to initialize your profile.")
    except Exception as e:
        logger.error(f"Error fetching balance: {e}")
        await update.message.reply_text("Error fetching balance.")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """View the user's bet history."""
    user = update.effective_user
    if not supabase:
        await update.message.reply_text("Database not connected.")
        return

    try:
        # First get user internal ID
        user_response = supabase.table("user_profiles").select("id").eq("telegram_id", user.id).execute()
        if not user_response.data:
            await update.message.reply_text("Please run /start first.")
            return

        user_id = user_response.data[0]['id']

        # Get last 5 bets
        history_resp = supabase.table("bet_ledger").select("*").eq("user_id", user_id).order("id", desc=True).limit(5).execute()

        if not history_resp.data:
            await update.message.reply_text("No bet history found.")
            return

        history_text = "Your last 5 bets:\n\n"
        for bet in history_resp.data:
            history_text += f"Market: {bet['market']}\nOdds: {bet['odds']}\nStatus: {bet['status']} | Result: {bet.get('result', 'N/A')}\n\n"

        await update.message.reply_text(history_text)
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        await update.message.reply_text("Error fetching history.")

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Toggle live notifications."""
    user = update.effective_user
    if not supabase:
        await update.message.reply_text("Database not connected.")
        return

    try:
        # Get current status
        user_response = supabase.table("user_profiles").select("id, signals_active").eq("telegram_id", user.id).execute()
        if not user_response.data:
            await update.message.reply_text("Please run /start first.")
            return

        current_status = user_response.data[0]['signals_active']
        new_status = not current_status

        # Update status
        supabase.table("user_profiles").update({"signals_active": new_status}).eq("telegram_id", user.id).execute()

        status_text = "ON" if new_status else "OFF"
        await update.message.reply_text(f"Live notifications are now {status_text}.")
    except Exception as e:
        logger.error(f"Error toggling signals: {e}")
        await update.message.reply_text("Error toggling signals.")
