from telegram import ParseMode
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

        formatted_text = f"Статистика:\nВсего лидгенов: <b>{n_leadgens}</b>\n\n"\
        f"Сегодня:\n\tКоннектов: <b>{result['today']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['today']['calls']}</b>\n"\
        f"\tСделок: <b>{result['today']['deals']}</b>\n"\
        f"\tЗарплаты: <b>{result['today']['earned']}</b>\n\n"\
        \
        f"Вчера:\n\tКоннектов: <b>{result['ystrdy']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['ystrdy']['calls']}</b>\n"\
        f"\tСделок: <b>{result['ystrdy']['deals']}</b>\n"\
        f"\tЗарплаты: <b>{result['ystrdy']['earned']}</b>\n\n"\
        \
        f"Эта неделя:\n\tКоннектов: <b>{result['this_week']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['this_week']['calls']}</b>\n"\
        f"\tСделок: <b>{result['this_week']['deals']}</b>\n"\
        f"\tЗарплаты: <b>{result['this_week']['earned']}</b>\n\n"\
        \
        f"Прошлая неделя:\n\tКоннектов: <b>{result['last_week']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['last_week']['calls']}</b>\n"\
        f"\tСделок: <b>{result['last_week']['deals']}</b>\n"\
        f"\tЗарплаты: <b>{result['last_week']['earned']}</b>\n\n"\
        \
        f"Этот месяц:\n\tКоннектов: <b>{result['this_month']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['this_month']['calls']}</b>\n"\
        f"\tСделок: <b>{result['this_month']['deals']}</b>\n"\
        f"\tЗарплаты: <b>{result['this_month']['earned']}</b>\n\n"\
        \
        f"Прошлый месяц:\n\tКоннектов: <b>{result['last_month']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['last_month']['calls']}</b>\n"\
        f"\tСделок: <b>{result['last_month']['deals']}</b>\n"\
        f"\tЗарплаты: <b>{result['last_month']['earned']}</b>\n\n"\
        \
        f"За все время:\n\tКоннектов: <b>{result['overall']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['overall']['calls']}</b>\n"\
        f"\tСделок: <b>{result['overall']['deals']}</b>\n"\
        f"\tЗарплаты: <b>{result['overall']['earned']}</b>\n\n"\
        # f"Год:\n\tКоннектов: <b>{result['year']['connects']}</b>\n"\
        # f"\tСозвонов: <b>{result['year']['calls']}</b>\n"\
        # f"\tСделок: <b>{result['year']['deals']}</b>\n"\
        # f"\tЗарплаты: <b>{result['year']['earned']}</b>\n\n"\

    else:
        leadgen_id = msg.split(")")[0]
        result = db_session.get_stats(leadgen_id)

        formatted_text = f"Статистика:\n"\
        f"Лидген: {msg}\n\n"\
        f"Сегодня:\n\tКоннектов: <b>{result['today']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['today']['calls']}</b>\n"\
        f"\tСделок: <b>{result['today']['deals']}</b>\n"\
        f"\tЗаработал(а): <b>{result['today']['earned']}</b>\n"\
        f"\tВ бане: <b>{result['today']['is_ban']}</b>\n"\
        f"\tРаботал: <b>{result['today']['is_work']}</b>\n\n"\
        \
        f"Вчера:\n\tКоннектов: <b>{result['ystrdy']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['ystrdy']['calls']}</b>\n"\
        f"\tСделок: <b>{result['ystrdy']['deals']}</b>\n"\
        f"\tЗаработал(а): <b>{result['ystrdy']['earned']}</b>\n"\
        f"\tВ бане: <b>{result['ystrdy']['is_ban']}</b>\n"\
        f"\tРаботал: <b>{result['ystrdy']['is_work']}</b>\n\n"\
        \
        f"Эта неделя:\n\tКоннектов: <b>{result['this_week']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['this_week']['calls']}</b>\n"\
        f"\tСделок: <b>{result['this_week']['deals']}</b>\n"\
        f"\tЗаработал(а): <b>{result['this_week']['earned']}</b>\n"\
        f"\tДней в бане: <b>{result['this_week']['days_ban']}</b>\n"\
        f"\tДней не в бане: <b>{result['this_week']['days_not_ban']}</b>\n\tДней работал: <b>{result['this_week']['days_work']}</b>\n"\
        f"\tДней не работал: <b>{result['this_week']['days_not_work']}</b>\n\n"\
        \
        f"Прошлая неделя:\n\tКоннектов: <b>{result['last_week']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['last_week']['calls']}</b>\n"\
        f"\tСделок: <b>{result['last_week']['deals']}</b>\n"\
        f"\tЗаработал(а): <b>{result['last_week']['earned']}</b>\n"\
        f"\tДней в бане: <b>{result['last_week']['days_ban']}</b>\n"\
        f"\tДней не в бане: <b>{result['last_week']['days_not_ban']}</b>\n\tДней работал: <b>{result['last_week']['days_work']}</b>\n"\
        f"\tДней не работал: <b>{result['last_week']['days_not_work']}</b>\n\n"\
        \
        f"Этот месяц:\n\tКоннектов: <b>{result['this_month']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['this_month']['calls']}</b>\n"\
        f"\tСделок: <b>{result['this_month']['deals']}</b>\n"\
        f"\tЗаработал(а): <b>{result['this_month']['earned']}</b>\n"\
        f"\tДней в бане: <b>{result['this_month']['days_ban']}</b>\n"\
        f"\tДней не в бане: <b>{result['this_month']['days_not_ban']}</b>\n\tДней работал: <b>{result['this_month']['days_work']}</b>\n"\
        f"\tДней не работал: <b>{result['this_month']['days_not_work']}</b>\n\n"\
        \
        f"Прошлый месяц:\n\tКоннектов: <b>{result['last_month']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['last_month']['calls']}</b>\n"\
        f"\tСделок: <b>{result['last_month']['deals']}</b>\n"\
        f"\tЗаработал(а): <b>{result['last_month']['earned']}</b>\n"\
        f"\tДней в бане: <b>{result['last_month']['days_ban']}</b>\n"\
        f"\tДней не в бане: <b>{result['last_month']['days_not_ban']}</b>\n\tДней работал: <b>{result['last_month']['days_work']}</b>\n"\
        f"\tДней не работал: <b>{result['last_month']['days_not_work']}</b>\n\n"\
        \
        f"За все время:\n\tКоннектов: <b>{result['overall']['connects']}</b>\n"\
        f"\tСозвонов: <b>{result['overall']['calls']}</b>\n"\
        f"\tСделок: <b>{result['overall']['deals']}</b>\n"\
        f"\tЗаработал(а): <b>{result['overall']['earned']}</b>\n"\
        f"\tДней в бане: <b>{result['overall']['days_ban']}</b>\n"\
        f"\tДней не в бане: <b>{result['overall']['days_not_ban']}</b>\n\tДней работал: <b>{result['overall']['days_work']}</b>\n"\
        f"\tДней не работал: <b>{result['overall']['days_not_work']}</b>\n\n"
        # f"Год:\n\tКоннектов: {result['year']['connects']}\n"\
        # f"\tСозвонов: {result['year']['calls']}\n"\
        # f"\tСделок: {result['year']['deals']}\n"\
        # f"\tЗаработал(а): {result['year']['earned']}\n"\
        # f"\tДней в бане: {result['year']['days_ban']}\n"\
        # f"\tДней не в бане: {result['year']['days_not_ban']}\n\tДней работал: {result['year']['days_work']}\n"\
        # f"\tДней не работал: {result['year']['days_not_work']}\n\n"\


    context.bot.send_message(
    chat_id=chat_id,
    text=formatted_text,
    parse_mode=ParseMode.HTML
    )

    return States.STATS_MENU
