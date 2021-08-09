from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from ...states import States
from ...data import text


# @restricted(None)
def admin(update: Update, context: CallbackContext):
    """ welcomes admin """
    chat_id = update.message.chat.id

    reply_markup = [
        [text["mssg_call"]],
        [text["get_stats"]]]

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["hi_admin"],
        reply_markup=markup,
    )
    return States.ADMIN_MENU