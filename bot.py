import os
import re
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

# BOT TOKEN Render Environment Variables se aayega
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not found!")

# Anti-link function
async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text
    if not text:
        return

    # Group admins ki list
    admins = await context.bot.get_chat_administrators(
        update.effective_chat.id
    )
    admin_ids = [admin.user.id for admin in admins]

    # Admin aur owner ke messages delete nahi honge
    if update.effective_user.id in admin_ids:
        return

    # Telegram links detect karo
    pattern = r"(https?://|www\.|t\.me/|telegram\.me/)"

    if re.search(pattern, text.lower()):
        try:
            await update.message.delete()
            print(f"Deleted message from user {update.effective_user.id}")
        except Exception as e:
            print(f"Delete error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            anti_link
        )
    )

    print("ParthTraderAlerts_Bot started...")
    app.run_polling(
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
