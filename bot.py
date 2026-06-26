import os
import re
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    # Admins ke messages delete nahi honge
    try:
        admins = await context.bot.get_chat_administrators(
            update.effective_chat.id
        )
        admin_ids = [admin.user.id for admin in admins]

        if update.effective_user.id in admin_ids:
            return
    except Exception as e:
        print(f"Admin check error: {e}")
        return

    text = update.message.text or ""

    # Telegram links detect
    pattern = r"(https?://|www\.|t\.me/)"

    if re.search(pattern, text.lower()):
        try:
            await update.message.delete()
            print(f"Deleted link from user {update.effective_user.id}")
        except Exception as e:
            print(f"Delete error: {e}")

def main():
    if not TOKEN:
        print("ERROR: BOT_TOKEN not found!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            anti_link,
        )
    )

    print("ParthTraderAlerts_Bot started...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
