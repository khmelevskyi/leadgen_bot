import os
import pytz
import datetime
from telegram import Update, chat
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardRemove

from ..data import text
from ..states import States
from ..database import db_session



def start(update: Update, context: CallbackContext):
    """ start command an msg """

    msg = update.message.text

    chat_id = update.message.chat.id

    context.bot.send_message(chat_id=chat_id, text=text["start"], reply_markup=ReplyKeyboardRemove())
    context.bot.send_message(chat_id=chat_id, text=text["main_menu"], reply_markup=ReplyKeyboardRemove())

    authorized_users = db_session.get_users_admins_list()
    authorized_users = [user[0] for user in authorized_users]

    if chat_id not in authorized_users: #DB.authorized_ids 
        context.bot.send_message(chat_id = chat_id, text = text["non-authorized"])
        return States.PASSWORD_CHECK

    return States.MAIN_MENU


def password_check(update: Update, context: CallbackContext):

    msg = update.message.text
    chat_id = update.message.chat.id
    
    authorized_users = db_session.get_users_admins_list()
    authorized_users = [user[0] for user in authorized_users]
    if chat_id in authorized_users: 
        context.bot.send_message(
            chat_id=chat_id,
            text=text["main_menu"],
        )
        return States.MAIN_MENU
    
    #admin_passwords = ["1212", "5070"]
    leadgen_password = "4224" #["4224", "1218"]  #from DB

    if msg in []:#admin_passwords:
        pass
    elif msg == leadgen_password:
        context.bot.send_message(chat_id = chat_id, text = text["enter_name"])
        return States.NAME_AND_SURNAME
    else:
        context.bot.send_message(chat_id = chat_id, text = text["wrong_password"])
        return States.PASSWORD_CHECK
    
    #context.bot.send_message(chat_id = chat_id, text = "Valid password, permissions of general user granted")


def name(update: Update, context: CallbackContext):

    msg = update.message.text
    chat_id = update.message.chat.id
    
    name = msg.split(" ")
    if len(name) != 2:
        context.bot.send_message(chat_id = chat_id, text = text["wrong_name_format"])
        return States.NAME_AND_SURNAME
    
    first_name = name[0]
    last_name = name[1]
    username = update.effective_chat.username
    chat_id = update.effective_chat.id
    time_registered = datetime.datetime.now(tz=pytz.timezone("Europe/Kiev"))

    context.user_data["first_name"] = first_name
    context.user_data["last_name"] = last_name
    context.user_data["username"] = username
    context.user_data["chat_id"] = chat_id
    context.user_data["time_registered"] = time_registered

    db_session.add_user(context.user_data)

    context.user_data.clear()

    context.bot.send_message(chat_id = chat_id, text = text["authorized_successfully"] % (str(first_name) + " " + str(last_name)))

    #send video

    context.bot.send_message(chat_id = chat_id, text = text["main_menu"])

    return States.MAIN_MENU


def main_menu(update: Update, context: CallbackContext):
    #msg = update.message.text
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id=chat_id, text=text["main_menu"], reply_markup=ReplyKeyboardRemove() )#f"You are in main menu\nEnter '/job' to report about your work or '/call' to plan new call\nYour message is: {msg}", reply_markup=ReplyKeyboardRemove())
    return States.MAIN_MENU


def everyday_ask_work(*args):
    context = args[0]

    users = db_session.get_users_list()

    for user in users:
        chat_id = user[0]
        context.bot.send_message(chat_id=chat_id, text=text["everyday_notification"], reply_markup=ReplyKeyboardRemove() )


def everyday_create_stat(*args):
    users_list = db_session.get_users_list()
    users_list = [user[0] for user in users_list]

    date = datetime.date.today()

    for user in users_list:
        db_session.create_user_stat(user, date)