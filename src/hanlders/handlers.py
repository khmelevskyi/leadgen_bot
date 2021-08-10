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

    if chat_id not in []: #DB.authorized_ids 
        context.bot.send_message(chat_id = chat_id, text = "You're non-authorized user. This is the password-check menu. Please, enter your password")
        return States.PASSWORD_CHECK

    return States.MAIN_MENU


def password_check(update: Update, context: CallbackContext):

    msg = update.message.text
    chat_id = update.message.chat.id
    
    #admin_passwords = ["1212", "5070"]
    leadgen_password = "4224" #["4224", "1218"]  #from DB

    if msg in []:#admin_passwords:
        pass
    elif msg == leadgen_password:
        context.bot.send_message(chat_id = chat_id, text = "Valid password. Please, enter your name and surname (Ivan Petrovich)", reply_markup=ReplyKeyboardRemove())
        return States.NAME_AND_SURNAME
    else:
        context.bot.send_message(chat_id = chat_id, text = "Invalid password. You have no permission to use the bot. Or try again")
        return States.PASSWORD_CHECK
    
    #context.bot.send_message(chat_id = chat_id, text = "Valid password, permissions of general user granted")


def name(update: Update, context: CallbackContext):

    msg = update.message.text
    chat_id = update.message.chat.id
    
    name = msg.split(" ")
    if len(name) != 2:
        context.bot.send_message(chat_id = chat_id, text = "wrong format, try again")
        return States.NAME_AND_SURNAME
    
    first_name = name[0]
    last_name = name[1]

    ###
    ###
    ###

    context.bot.send_message(chat_id = chat_id, text = "congrats, you authorized successfully")

    #send video

    return States.MAIN_MENU


def main_menu(update: Update, context: CallbackContext):
    msg = update.message.text
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text=f"Your message is: {msg}", reply_markup=ReplyKeyboardRemove())
    return States.MAIN_MENU