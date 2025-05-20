from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from states import State

conversation_states: dict[int, dict[str]] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm WishBot and I can save your wishes!. You can choose needed action from menu.")


async def create_wish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['id'] = update.message.from_user.id
    await update.message.reply_text("Let's create Wish! Enter your wish name:'")
    return State.WISH_NAME


async def set_wish_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text or update.message.text == '':
        return State.START
    context.user_data['name'] = update.message.text
    await update.message.reply_text('Enter your wish description:')
    return State.WISH_DESCRIPTION


async def set_wish_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['description'] = update.message.text
    await update.message.reply_text('Enter your wish url:')
    return State.WISH_URL


async def set_wish_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['url'] = update.message.text
    print('[wish]', context.user_data)
    await update.message.reply_text('Congrats! Your Wish saved!')
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
