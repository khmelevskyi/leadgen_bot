from telegram import ParseMode
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

    admins = db_session.get_admins(["superadmin", "leadgen", "sales"])
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    reply_markup = [
        [text["mssg_call"], text["get_stats"]],
        [text["del_user"], text["make_admin"]],
        [text["push_mssg"]],
        [text["back"]]]

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["hi_admin"],
        reply_markup=markup,
    )
    return States.ADMIN_MENU


### make admin
def make_admin(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin"])
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    users_list = db_session.get_users_admins_name()

    reply_markup = []

    for user in users_list:
        user = f"{user[0]}) - {user[1]} {user[2]}"
        reply_markup.append([user])

    reply_markup.append([text["back"]])

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text="Выберите пользователя:",
        reply_markup=markup,
    )
    return States.MAKE_ADMIN

def make_admin_role(update: Update, context: CallbackContext):

    msg = update.message.text

    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin"])
    # n_admins = len(admins)
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    new_admin_chat_id = msg.split(")")[0]

    context.user_data["new_admin_chat_id"] = new_admin_chat_id

    reply_markup = [
        ["superadmin"],
        ["leadgen"],
        ["sales"]
    ]

    reply_markup.append([text["back"]])

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text="Выберите роль админа",
        reply_markup=markup,
    )

    return States.MAKE_ADMIN_SAVE

def make_admin_save(update: Update, context: CallbackContext):

    msg = update.message.text

    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin"])
    # n_admins = len(admins)
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    new_admin_chat_id = context.user_data["new_admin_chat_id"]

    db_session.make_admin(new_admin_chat_id, msg)

    context.user_data.pop("new_admin_chat_id")

    context.bot.send_message(
        chat_id=chat_id,
        text="Пользователь успешно добавлен в админы!",
    )

    return admin(update, context)


#### delete user
def del_user(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin"])
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    users_list = db_session.get_users_admins_name()

    reply_markup = []

    for user in users_list:
        user = f"{user[0]}) - {user[1]} {user[2]}"
        reply_markup.append([user])

    reply_markup.append([text["back"]])

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text="Выберите пользователя для удаления (опасно📛):",
        reply_markup=markup,
    )
    return States.DEL_USER


def del_user_save(update: Update, context: CallbackContext):

    msg = update.message.text

    del_user_chat_id = msg.split(")")[0]

    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin"])
    # n_admins = len(admins)
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    db_session.delete_user(del_user_chat_id)

    context.bot.send_message(
        chat_id=chat_id,
        text="Пользователь успешно удален!",
    )

    return admin(update, context)


### push message
def push_mssg(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin"])
    # n_admins = len(admins)
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    reply_markup = [
        ["Всем"],
        ["Только лидгенам"],
        ["Только админам"],
    ]

    reply_markup.append([text["back"]])

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text="Выберите кому отправить сообщение:",
        reply_markup=markup,
    )

    return States.PUSH_MSSG

def push_mssg_text(update: Update, context: CallbackContext):

    mssg = update.message.text
    
    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin"])
    # n_admins = len(admins)
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    context.user_data["send_mssg_to"] = mssg

    reply_markup = []

    reply_markup.append([text["back"]])

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text="Напишите сообщение для отправки:",
        reply_markup=markup,
    )

    return States.PUSH_MSSG_FINAL


def push_mssg_final(update: Update, context: CallbackContext):

    mssg = update.message.text
    
    chat_id = update.message.chat.id

    admins = db_session.get_admins(["superadmin"])
    # n_admins = len(admins)
    admins = [admin[0] for admin in admins]

    #Check
    if chat_id not in admins: #***list of admin users' chat_ids from DB***
        context.bot.send_message(chat_id=chat_id, text=text["not_an_admin"])
        return States.MAIN_MENU

    receiver = context.user_data["send_mssg_to"]

    if receiver == "Всем":
        users = db_session.get_users_admins_list()
        users = [user[0] for user in users]

        for user in users:
            context.bot.send_message(
                chat_id=user,
                text=mssg,
                parse_mode=ParseMode.HTML
            )
    elif receiver == "Только лидгенам":
        users = db_session.get_users_list()
        users = [user[0] for user in users]

        for user in users:
            context.bot.send_message(
                chat_id=user,
                text=mssg,
                parse_mode=ParseMode.HTML
            )
    elif receiver == "Только админам":
        users = db_session.get_admins(["superadmin", "leadgen", "sales"])
        users = [user[0] for user in users]

        for user in users:
            context.bot.send_message(
                chat_id=user,
                text=mssg,
                parse_mode=ParseMode.HTML
            )

    return admin(update, context)
