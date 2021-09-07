import datetime
from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from ...hanlders import main_menu
from ...database import db_session
from ...states import States
from ...data import text



def report(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    authorized_users = db_session.get_users_admins_list()
    authorized_users = [user[0] for user in authorized_users]
    if chat_id not in authorized_users: 
        context.bot.send_message(
            chat_id=chat_id,
            text=text["not_a_leadgen"],
        )
        return States.PASSWORD_CHECK
    
    date_now = datetime.date.today()

    user_stats = db_session.get_user_stat(chat_id, date_now)
    print(user_stats) 
    ## user_stat[0][7] = work | True or False
    ## user_stat[0][3] = calls | 0, 1, ..
    if user_stats and user_stats[0][7] == True: # checks if stat for this user and this date exists
        reply_markup = [                      # and checks whether he worked today or not
            [text["yes"]],
            [text["no"]]
        ]

        markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

        context.bot.send_message(
            chat_id=chat_id,
            text=text["want_new_connects"],#"Вы уже вводили данные о своей работе сегодня, хотите изменить количество коннектов?",
            reply_markup=markup,
        )
        return States.CHANGE_CONNECTS_WANT

    elif user_stats and user_stats[0][7] == False:
        context.bot.send_message(
            chat_id=chat_id,
            text=text["already_reported"],#"Вы уже вводили данные о своей работе сегодня,указав, что не работали сегодня!",
            reply_markup=ReplyKeyboardRemove(),
        )
        return States.MAIN_MENU

    reply_markup = [
        [text["no_w_no_b"]],
        [text["no_w_b"]],
        [text["w_b"]],
        [text["w_no_b"]],
        [text["back"]],
    ]

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["how_worked"],
        reply_markup=markup,
    )
    return States.REPORT


def report_options(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id
    msg = update.message.text

    if msg == text["no_w_no_b"]:
        connects = 0 # didn't work = no connects
        ban = False
        work = False
        added_at = datetime.date.today()

        context.user_data["leadgen_id"] = chat_id
        context.user_data["connects"] = connects
        context.user_data["ban"] = ban
        context.user_data["work"] = work
        context.user_data["added_at"] = added_at

        db_session.add_user_stat(context.user_data)
        context.user_data.clear()

        context.bot.send_message(chat_id=chat_id, text=text["report_thanks"], reply_markup = ReplyKeyboardRemove())
        return main_menu(update, context)

    elif msg == text["no_w_b"]:
        connects = 0 # didn't work = no connects
        ban = True
        work = False
        added_at = datetime.date.today()

        context.user_data["leadgen_id"] = chat_id
        context.user_data["connects"] = connects
        context.user_data["ban"] = ban
        context.user_data["work"] = work
        context.user_data["added_at"] = added_at

        db_session.add_user_stat(context.user_data)
        context.user_data.clear()

        context.bot.send_message(chat_id=chat_id, text=text["report_thanks"], reply_markup = ReplyKeyboardRemove())
        return main_menu(update, context)

    elif msg == text["w_b"]:
        ban = True
        work = True
        added_at = datetime.date.today()

        context.user_data["leadgen_id"] = chat_id
        context.user_data["ban"] = ban
        context.user_data["work"] = work
        context.user_data["added_at"] = added_at

        context.bot.send_message(chat_id=chat_id, text=text["enter_connects"], reply_markup = ReplyKeyboardRemove())
        return States.CONNECTS

    elif msg == text["w_no_b"]:
        ban = False
        work = True
        added_at = datetime.date.today()

        context.user_data["leadgen_id"] = chat_id
        context.user_data["ban"] = ban
        context.user_data["work"] = work
        context.user_data["added_at"] = added_at

        context.bot.send_message(chat_id=chat_id, text=text["enter_connects"], reply_markup = ReplyKeyboardRemove())
        return States.CONNECTS


def connects(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id
    msg = update.message.text

    try:
        connects = int(msg)
    except:
        context.bot.send_message(chat_id=chat_id, text=text["connects_nan"], reply_markup = ReplyKeyboardRemove())
        return States.CONNECTS
    
    ban = context.user_data["ban"]
    context.user_data["connects"] = connects

    db_session.add_user_stat(context.user_data)
    context.user_data.clear()

    context.bot.send_message(chat_id=chat_id, text=text["report_thanks"], reply_markup = ReplyKeyboardRemove())
    return main_menu(update, context)


def change_connects_want(update: Update, context: CallbackContext):

    chat_id = update.message.chat_id

    context.bot.send_message(chat_id=chat_id, text=text["enter_new_connects"], reply_markup = ReplyKeyboardRemove())

    return States.CHANGE_CONNECTS

def change_connects(update: Update, context: CallbackContext):

    chat_id = update.message.chat_id
    date_now = datetime.date.today()
    try:
        msg = int(update.message.text)
    except:
        context.bot.send_message(chat_id=chat_id, text=text["connects_nan"], reply_markup = ReplyKeyboardRemove())
        return States.CHANGE_CONNECTS

    db_session.change_user_stat_connects(chat_id, date_now, msg)
    context.user_data.clear()

    context.bot.send_message(chat_id=chat_id, text= "Количество коннектов изменено!", reply_markup = ReplyKeyboardRemove())

    return main_menu(update, context)
