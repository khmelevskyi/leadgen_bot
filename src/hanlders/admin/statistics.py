from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
import pandas as pd

from ...database import db_session
from ...database import Calls
from ...states import States
from ...data import text


def get_stats(update: Update, context: CallbackContext):
    

    db_session.get_stats()

    chat_id = update.message.chat.id

    admins = db_session.get_admins()
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.PASSWORD_CHECK

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
    return States.ADMIN_MENU


# def query_to_dict(rset):
#     result = defaultdict(list)
#     for obj in rset:
#         instance = inspect(obj)
#         for key, x in instance.attrs.items():
#             result[key].append(x.value)
#     return result