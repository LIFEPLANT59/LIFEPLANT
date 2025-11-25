import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("Токен бота не найден! Проверьте файл .env")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! 👋"
        "\nЯ работаю на python-telegram-bot v20.7"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "<b>Доступные команды:</b>\n"
        "/start - начать взаимодействие\n"
        "/help - показать эту справку\n\n"
        "<i>Пишите текст - я повторю!</i>"
    )
    await update.message.reply_text(help_text, parse_mode="HTML")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text[:100]
    await update.message.reply_text(
        f"🔹 <b>Эхо-сообщение:</b>\n<i>{message_text}</i>",
        parse_mode="HTML"
    )

def main():
    application = (
        Application.builder()
        .token(TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )
    print("🚀 Бот запущен в режиме polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
    