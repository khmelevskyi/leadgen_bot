from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

from ...states import States
from ...data import text
from ...database import db_session


# @restricted(None)
def admin(update: Update, context: CallbackContext):
    """ welcomes admin """
    chat_id = update.message.chat.id

    admins = db_session.get_admins()
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.PASSWORD_CHECK

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