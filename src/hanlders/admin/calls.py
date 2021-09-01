from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from .admin import admin

from ...states import States
from ...data import text
from ...database import db_session


def pick_call(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    calls = db_session.get_calls_list()
    #print(calls)
    """
    print("\n\n\n")
    for i, call in enumerate(calls):
        print(f"{i} ------ {call}")
        print("\n")
    print("-----------------------------------------------")
    print("\n")
    """

    reply_markup = []

    #1
    
    for call in calls:
        call = f"{call[0]}) - {call[1].date()} - {call[1].time()} - {call[2]}"
        reply_markup.append([call])
    
    #
    """
    for i, call in enumerate(calls):
        call = ""
    """
    if reply_markup == []:
        context.bot.send_message(
            chat_id=chat_id,
            text=text["no_calls_for_now"], 
        )
        return States.ADMIN_MENU

    reply_markup.append([text["back"]])

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["choose_call"],
        reply_markup=markup,
    )
    return States.ADMIN_CALL_CHOSEN


def get_call(option, calls):
    for call in calls:
        if option == call[0]:
            print(call)
            return call
    return None


def call_feedback(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id
    msg = update.message.text

    
    try:
        msg = msg.split(")")
        option = int(msg[0])
    except ValueError:
        context.bot.send_message(chat_id=chat_id, text=text["err_unexpected_type"])
        return pick_call(update, context)

    calls = db_session.get_calls_list()
    call = get_call(option, calls)
    if call != None:
        context.user_data["chosen_call"] = call
    else:
        return pick_call(update, context)

    reply_markup = [
        [text["yes"]],
        [text["no"]]
    ]

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["has_call_been"],
        reply_markup=markup,
    )
    return States.HAS_CALL_BEEN


def call_yes(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id

    admin_reply_markup = [ [text["mssg_call"] ], [ text["get_stats"] ] ]
    admin_markup = ReplyKeyboardMarkup(keyboard=admin_reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["call_yes_admin_thanks"],
        reply_markup=admin_markup,
    )

    chosen_call = context.user_data["chosen_call"]
    # print(chosen_call)
    db_session.call_done(chosen_call)

    context.bot.send_message(
        chat_id=chosen_call[3],
        text=text["call_yes_lead_thanks"],
    )
    context.user_data.pop("chosen_call")
    return admin(update, context)


def call_no(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text=text["call_no_admin"],
        reply_markup=ReplyKeyboardRemove()
    )

    return States.CALL_NO_DESCRIPTION


def send_description(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id
    msg = update.message.text

    chosen_call = context.user_data["chosen_call"]
    db_session.delete_call(chosen_call)

    admin_reply_markup = [ [text["mssg_call"] ], [ text["get_stats"] ] ]
    admin_markup = ReplyKeyboardMarkup(keyboard=admin_reply_markup, resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat_id,
        text=text["call_no_admin_descr_thx"],
        reply_markup=admin_markup,
    )

    context.bot.send_message(
        chat_id=chosen_call[3],
        text=text["call_no_lead"] + msg + "\"",
        #reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.pop("chosen_call")
    return admin(update, context)