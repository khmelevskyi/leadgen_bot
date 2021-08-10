from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from ...states import States
from ...data import text



def plan_call(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    if chat_id not in [chat_id]: #DB.leadgens_chat_ids:
        context.bot.send_message(
            chat_id=chat_id,
            text="You are not a leadgen(call.py)",
        )
        return States.PASSWORD_CHECK
    
    context.bot.send_message(
        chat_id=chat_id,
        text=text["leadgen_call_date"],
        reply_markup=ReplyKeyboardRemove(),
    )
    return States.CALL_PLAN_DATE




def plan_call_date(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id
    msg = update.message.text

    if len(msg) != 5 or msg[2] != ".": #check
        context.bot.send_message(
            chat_id=chat_id,
            text="Invalid date, insert again (call.py)",
            reply_markup=ReplyKeyboardRemove(),
        )
        return States.CALL_PLAN_DATE
    
    context.user_data["new_call_date"] = msg

    context.bot.send_message(
        chat_id=chat_id,
        text=text["leadgen_call_time"],
        reply_markup=ReplyKeyboardRemove(),
    )
    return States.CALL_PLAN_TIME




def plan_call_time(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id
    msg = update.message.text

    if len(msg) != 5 or msg[2] != ":": #check
        context.bot.send_message(
            chat_id=chat_id,
            text="Invalid time, insert again (call.py)",
            reply_markup=ReplyKeyboardRemove(),
        )
        return States.CALL_PLAN_TIME
    
    context.user_data["new_call_time"] = msg

    context.bot.send_message(
        chat_id=chat_id,
        text=text["leadgen_call_link"],
        reply_markup=ReplyKeyboardRemove(),
    )
    return States.CALL_PLAN_LINK




def plan_call_link(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id
    msg = update.message.text

    #check link:
    if msg.find("linkedin.com") == -1:
        context.bot.send_message(
            chat_id=chat_id,
            text="Invalid link, insert again (call.py)",
            reply_markup=ReplyKeyboardRemove(),
        )
        return States.CALL_PLAN_LINK

    context.bot.send_message(
        chat_id=chat_id,
        text=text["leadgen_call_ok"],
        reply_markup=ReplyKeyboardRemove(),
    )

    context.user_data["new_call_link"] = msg

    call_date = context.user_data["new_call_date"]
    call_time = context.user_data["new_call_time"]
    call_link = context.user_data["new_call_link"]
    call_creator_chat_id = chat_id

    ###
    ###
    ###

    for admin_id in [chat_id]: #DB.admin_ids:
        context.bot.send_message(
            chat_id = admin_id,
            text=text["admin_new_call_notification"] + f"Date: {call_date}\nTime: {call_time}\nLink: {call_link}"
        )
    return States.PASSWORD_CHECK
