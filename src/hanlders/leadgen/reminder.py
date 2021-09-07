# import pytz
import datetime
from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup

from ...data import text, TIME_ZONE
from ...states import States
from ...database import db_session
# from ...hanlders import main_menu

### uncomment only to create default reminder time, run it only for the first time!
### default reminder time setter
# users = db_session.get_users_list()
# for user in users:
#     user_id = user[0]
#     db_session.add_reminder_time(user_id, datetime.time(hour=21, tzinfo=pytz.timezone("Europe/Kiev")))
###

def reminder(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    user = db_session.get_user(chat_id)

    ### ----- from DB -----
    reminder_time = user.reminder_time

    reply_markup = [
        [text["change_time"]],
        [text["remove_reminder"]],
        [text["back"]]
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    if reminder_time == None:
        context.bot.send_message(
            chat_id = chat_id,
            text=text["your_reminder_off"],
            reply_markup = markup
        )
    else:
        context.bot.send_message(
            chat_id = chat_id,
            text = text["your_reminder_time_is"].format(reminder_time.strftime('%H:%M')),
            reply_markup = markup
        )
    
    return States.CHANGE_TIME_WANT


def change_time(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    reply_markup = [
        [text["cancel"]]
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id = chat_id,
        text = text["insert_new_time"],
        reply_markup=markup
    )
    return States.CHANGE_TIME_INSERT


def change_time_insert(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id
    msg = update.message.text

    try:
        new_time = int(msg)
    except:
        context.bot.send_message(
            chat_id = chat_id,
            text = text["reminder_invalid_time"]
        )
        return States.CHANGE_TIME_INSERT

    if 0<=new_time<=24:

        new_reminder = datetime.time(hour=new_time, tzinfo=TIME_ZONE)
        ### ----- save new_time to DB -----
        db_session.add_reminder_time(chat_id, new_reminder)

        context.bot.send_message(
            chat_id = chat_id,
            text = text["new_time_set"]
        )
        return reminder(update, context)
    
    else:
        context.bot.send_message(
            chat_id = chat_id,
            text = text["reminder_invalid_time"]
        )
        return States.CHANGE_TIME_INSERT


def remove_reminder(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    reply_markup = [
        [text["yes"]],
        [text["cancel"]]
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id = chat_id,
        text = text["remove_reminder_sure"],
        reply_markup=markup
    )
    return States.REMOVE_REMINDER

def remove_reminder_approve(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    db_session.remove_reminder_time(chat_id)

    context.bot.send_message(
        chat_id = chat_id,
        text = text["reminder_removed"],
    )

    return reminder(update, context)
