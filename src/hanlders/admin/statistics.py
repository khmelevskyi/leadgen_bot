from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
import pandas as pd

from ...database import db_session
from ...database import Calls
from ...states import States
from ...data import text


def get_stats(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin", "leadgen"])
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    users_list = db_session.get_users_name()

    reply_markup = []

    for user in users_list:
        user = f"{user[0]}) - {user[1]} {user[2]}"
        reply_markup.append([user])

    reply_markup.append(["Все"])
    reply_markup.append([text["back"]])

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text="Выберите лидгена или всех",
        reply_markup=markup,
    )
    return States.STATS_MENU


def show_stats(update: Update, context: CallbackContext):

    msg = update.message.text

    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin", "leadgen"])
    # n_admins = len(admins)
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    users_list = db_session.get_users_name()
    n_leadgens = len(users_list)

    if msg == "Все":
        result = db_session.get_stats()
        # print(result)

        formatted_text = f"Статистика:\nВсего лидгенов: {n_leadgens}\n\n"\
        f"Сегодня:\n\tКоннектов: {result['today']['connects']}\n"\
        f"\tСозвонов: {result['today']['calls']}\n\n"\
        f"Вчера:\n\tКоннектов: {result['ystrdy']['connects']}\n"\
        f"\tСозвонов: {result['ystrdy']['calls']}\n\n"\
        f"Этот месяц:\n\tКоннектов: {result['this_month']['connects']}\n"\
        f"\tСозвонов: {result['this_month']['calls']}\n\n"\
        f"Прошлый месяц:\n\tКоннектов: {result['last_month']['connects']}\n"\
        f"\tСозвонов: {result['last_month']['calls']}\n\n"\
        f"Год:\n\tКоннектов: {result['year']['connects']}\n"\
        f"\tСозвонов: {result['year']['calls']}\n\n"\
        f"За все время:\n\tКоннектов: {result['overall']['connects']}\n"\
        f"\tСозвонов: {result['overall']['calls']}\n\n"

    else:
        leadgen_id = msg.split(")")[0]
        result = db_session.get_stats(leadgen_id)

        formatted_text = f"Статистика:\n"\
        f"Лидген: {msg}\n\n"\
        f"Сегодня:\n\tКоннектов: {result['today']['connects']}\n"\
        f"\tСозвонов: {result['today']['calls']}\n\tВ бане: {result['today']['is_ban']}\n"\
        f"\tРаботал: {result['today']['is_work']}\n\n"\
        f"Вчера:\n\tКоннектов: {result['ystrdy']['connects']}\n"\
        f"\tСозвонов: {result['ystrdy']['calls']}\n\tВ бане: {result['ystrdy']['is_ban']}\n"\
        f"\tРаботал: {result['ystrdy']['is_work']}\n\n"\
        f"Этот месяц:\n\tКоннектов: {result['this_month']['connects']}\n"\
        f"\tСозвонов: {result['this_month']['calls']}\n\tДней в бане: {result['this_month']['days_ban']}\n"\
        f"\tДней не в бане: {result['this_month']['days_not_ban']}\n\tДней работал: {result['this_month']['days_work']}\n"\
        f"\tДней не работал: {result['this_month']['days_not_work']}\n\n"\
        f"Прошлый месяц:\n\tКоннектов: {result['last_month']['connects']}\n"\
        f"\tСозвонов: {result['last_month']['calls']}\n\tДней в бане: {result['last_month']['days_ban']}\n"\
        f"\tДней не в бане: {result['last_month']['days_not_ban']}\n\tДней работал: {result['last_month']['days_work']}\n"\
        f"\tДней не работал: {result['last_month']['days_not_work']}\n\n"\
        f"Год:\n\tКоннектов: {result['year']['connects']}\n"\
        f"\tСозвонов: {result['year']['calls']}\n\tДней в бане: {result['year']['days_ban']}\n"\
        f"\tДней не в бане: {result['year']['days_not_ban']}\n\tДней работал: {result['year']['days_work']}\n"\
        f"\tДней не работал: {result['year']['days_not_work']}\n\n"\
        f"За все время:\n\tКоннектов: {result['overall']['connects']}\n"\
        f"\tСозвонов: {result['overall']['calls']}\n\tДней в бане: {result['overall']['days_ban']}\n"\
        f"\tДней не в бане: {result['overall']['days_not_ban']}\n\tДней работал: {result['overall']['days_work']}\n"\
        f"\tДней не работал: {result['overall']['days_not_work']}\n\n"


    context.bot.send_message(
    chat_id=chat_id,
    text=formatted_text
    )

    return States.STATS_MENU
