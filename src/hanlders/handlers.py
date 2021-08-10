from telegram import Update, chat
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardRemove

from ..data import text
from ..states import States


def end_func(chat_id):
    pass


def start(update: Update, context: CallbackContext):
    """ start command an msg """

    msg = update.message.text

    chat_id = update.message.chat.id

    context.bot.send_message(chat_id=chat_id, text=text["start"], reply_markup=ReplyKeyboardRemove())

    return States.PASSWORD_CHECK


def password_check(update: Update, context: CallbackContext):

    msg = update.message.text

    chat_id = update.message.chat.id

    context.bot.send_message(chat_id=chat_id, text=f"Your message is: {msg}", reply_markup=ReplyKeyboardRemove())

    return States.PASSWORD_CHECK