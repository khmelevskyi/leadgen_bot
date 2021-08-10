from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from ...states import States
from ...data import text


def pick_call_old(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id
    
    context.bot.send_message(
        chat_id=chat_id,
        text=text["choose_call"],
    )

    test_date = "09.08"
    test_time = "12:00"
    test_emoji = ":question:"
    
    #DB.calls = [call1, call2,] (-> obj)
    call_list = ""
    cntr = 1
    """
    for call in DB.calls[-10:]:
        if call.was_succesful == True:
            emoji = ":check_mark:"
        else if call.was_succesful == False:
            emoji = ":x:"
        else if call.was_succesful == None:
            emoji = ":question:"
        call_list += f"{cntr})📞 {call.date}, {call.time} {emoji}\n"
        cntr += 1
    """
    call_list += f"{cntr})📞 {test_date}, {test_time} {test_emoji}\n"

    context.bot.send_message(
        chat_id=chat_id,
        text=call_list,
        reply_markup=ReplyKeyboardRemove()
    )
    return States.ADMIN_CALL_CHOSEN




def pick_call(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    reply_markup = []
    cntr = 1
    """
    for call in DB.calls[-9:]:
        if call.was_succesful is None:
            emoji = ":question:"
        elif call.was_succesful:
            emoji = ":check_mark:"
        elif not call.was_succesful:
            emoji = ":x:"
        k_element = f"{cntr})📞 {call.date}, {call.time} {emoji}"
        cntr += 1
        reply_markup.append([k_element])
    """
    t_date = "24.05"
    t_time = "12:00"
    t_emoji = "**?**"
    k_element = f"{cntr})📞 {t_date}, {t_time} {t_emoji}"
    reply_markup.append([k_element])


    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["choose_call"],
        reply_markup=markup,
    )
    return States.ADMIN_CALL_CHOSEN




def call_feedback(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id
    msg = update.message.text

    admin_reply_markup = [ [text["mssg_call"] ], [ text["get_stats"] ] ]
    admin_markup = ReplyKeyboardMarkup(keyboard=admin_reply_markup, resize_keyboard=True)

    """
    try:
        option = int(msg[0])
    except ValueError:
        context.bot.send_message(chat_id=chat_id, text=text["err_unexpected_type"],reply_markup=admin_markup,)
        return States.ADMIN_MENU
    """
    option = int(msg[0])

    #DB.calls[-9:][option-1].
    #context.user_data["chosen_call"] = DB.calls[-9:][option-1]

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

    #chosen_call = context.user_data["chosen_call"]
    #chosen_call.was_succesful = True

    context.bot.send_message(
        chat_id=chat_id,
        #chat_id=chosen_call.creator_chat_id,
        text=text["call_yes_lead_thanks"],
    )
    return States.ADMIN_MENU




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

    #chosen_call = context.user_data["chosen_call"]
    #chosen_call.was_succesful = False

    admin_reply_markup = [ [text["mssg_call"] ], [ text["get_stats"] ] ]
    admin_markup = ReplyKeyboardMarkup(keyboard=admin_reply_markup, resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat_id,
        text=text["call_no_admin_descr_thx"],
        reply_markup=admin_markup,
    )

    context.bot.send_message(
        chat_id=chat_id,
        #chat_id=chosen_call.creator_chat_id,
        text=text["call_no_lead"] + msg + "\"",
        #reply_markup=ReplyKeyboardRemove()
    )
    return States.ADMIN_MENU