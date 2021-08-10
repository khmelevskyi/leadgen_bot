from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from ...states import States
from ...data import text



def report(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    reply_markup = [
        [text["no_w_no_b"]],
        [text["no_w_b"]],
        [text["w_b"]],
        [text["w_no_b"]],
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

    context.user_data["ban"] = None
    connects = 0
    if msg == text["no_w_no_b"]:
        ban = False
        ###
        ###
        ###
        #context.bot.send_message(chat_id=chat_id, text=text["none"])
        context.bot.send_message(chat_id=chat_id, text= f"Ban: {ban}, connects:{connects}", reply_markup = ReplyKeyboardRemove())
        return States.MAIN_MENU

    elif msg == text["no_w_b"]:
        ban = True
        ###
        ###
        ###
        #context.bot.send_message(chat_id=chat_id, text=text["none"])
        context.bot.send_message(chat_id=chat_id, text= f"Ban: {ban}, connects:{connects}", reply_markup = ReplyKeyboardRemove())
        return States.MAIN_MENU

    elif msg == text["w_b"]:
        context.user_data["ban"] = True
        context.bot.send_message(chat_id=chat_id, text="enter", reply_markup = ReplyKeyboardRemove())
        return States.CONNECTS

    elif msg == text["w_no_b"]:
        context.user_data["ban"] = False
        context.bot.send_message(chat_id=chat_id, text="enter", reply_markup = ReplyKeyboardRemove())
        return States.CONNECTS


def connects(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id
    msg = update.message.text

    try:
        connects = int(msg)
    except:
        context.bot.send_message(chat_id=chat_id, text="NaN!", reply_markup = ReplyKeyboardRemove())
        return States.CONNECTS
    
    ban = context.user_data["ban"]

    ###
    ###
    ###

    context.bot.send_message(chat_id=chat_id, text= f"Ban: {ban}, connects:{connects}", reply_markup = ReplyKeyboardRemove())
    return States.MAIN_MENU