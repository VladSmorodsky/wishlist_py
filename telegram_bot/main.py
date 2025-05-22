import os

from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

from handlers import start, create_wish, cancel, set_wish_name, set_wish_description, set_wish_url, get_my_wishlist
from logger import get_logger
from states import State

load_dotenv()

logger = get_logger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def setup_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start conversation"),
        BotCommand("create_wish", "Create wish"),
        BotCommand("cancel", "End the conversation"),
        BotCommand("get_my_wishlist", "Get My Wishes"),
    ])


handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
        CommandHandler("create_wish", create_wish),
        CommandHandler("get_my_wishlist", get_my_wishlist),
        CommandHandler("cancel", cancel)],
    states={
        State.CREATE_WISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_wish)],
        State.WISH_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_wish_name)],
        State.WISH_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_wish_description)],
        State.WISH_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_wish_url)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

logger.info('Bot is running...')

app = ApplicationBuilder().token(TOKEN).post_init(setup_commands).build()
app.add_handler(handler)

app.run_polling()
