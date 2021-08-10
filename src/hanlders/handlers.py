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

    if chat_id not in [chat_id]: #DB.authorized_ids 
        context.bot.send_message(chat_id = chat_id, text = "You're non-authorized user. This is the password-check menu. Please, enter your password")
        return States.PASSWORD_CHECK

    return States.MAIN_MENU


def password_check(update: Update, context: CallbackContext):

    msg = update.message.text
    chat_id = update.message.chat.id
    
    user_passwords = ["0000","1111", "1234"] #from DB
    admin_passwords = ["1212", "5070"]
    leadgen_passwords = ["4224", "1218"]
    if msg in user_passwords:
        pass
    elif msg in admin_passwords:
        pass
    elif msg in leadgen_passwords:
        pass
    else:
        context.bot.send_message(chat_id = chat_id, text = "Invalid password. You have no permission to use the bot. Or try again")
        return States.PASSWORD_CHECK
    
    #context.bot.send_message(chat_id = chat_id, text = "Valid password, permissions of general user granted")


def main_menu(update: Update, context: CallbackContext):
    msg = update.message.text
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text=f"Your message is: {msg}", reply_markup=ReplyKeyboardRemove())
    return States.MAIN_MENU