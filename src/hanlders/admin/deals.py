from telegram import Update
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from .admin import admin

from ...states import States
from ...data import text
from ...database import db_session


def pick_deal(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    deals = db_session.get_deals_list()

    reply_markup = []
    
    for deal in deals:
        deal = f"{deal[0]}) - {deal[2]}"
        reply_markup.append([deal])
    
    if reply_markup == []:
        context.bot.send_message(
            chat_id=chat_id,
            text=text["no_deals_for_now"], 
        )
        return States.ADMIN_MENU

    reply_markup.append([text["back"]])

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["choose_deal"],
        reply_markup=markup,
    )
    return States.ADMIN_DEAL_CHOSEN


def get_deal(option, deals):
    for deal in deals:
        if option == deal[0]:
            print(deal)
            return deal
    return None


def deal_feedback(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id
    msg = update.message.text

    
    try:
        msg = msg.split(")")
        option = int(msg[0])
    except ValueError:
        context.bot.send_message(chat_id=chat_id, text=text["err_unexpected_type"])
        return pick_deal(update, context)

    deals = db_session.get_deals_list()
    deal = get_deal(option, deals)
    if deal != None:
        context.user_data["chosen_deal"] = deal
    else:
        return pick_deal(update, context)

    reply_markup = [
        [text["yes"]],
        [text["no"]],
        [text["back"]]
    ]

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["has_deal_been"],
        reply_markup=markup,
    )
    return States.HAS_DEAL_BEEN


def deal_no(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text=text["deal_no_admin"],
        reply_markup=ReplyKeyboardRemove()
    )

    return States.DEAL_NO_DESCRIPTION


def send_deal_description(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id
    msg = update.message.text

    chosen_deal = context.user_data["chosen_deal"]
    db_session.delete_deal(chosen_deal)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["deal_no_admin_descr_thx"],
    )

    context.bot.send_message(
        chat_id=chosen_deal[2],
        text=text["deal_no_lead"] + msg + "\"",
        #reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.pop("chosen_deal")
    return admin(update, context)


def deal_yes(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text=text["deal_summ"],
        reply_markup=ReplyKeyboardRemove()
    )

    return States.DEAL_YES_SUMM

def deal_yes_summ(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    mssg = update.message.text

    context.user_data["deal_summ"] = mssg

    context.bot.send_message(
        chat_id=chat_id,
        text=text["deal_percent"],
        reply_markup=ReplyKeyboardRemove()
    )

    return States.DEAL_YES_PERCENT

def deal_yes_percent(update: Update, context: CallbackContext):

    chat_id = update.message.chat.id

    mssg = update.message.text

    deal_percent = context.user_data["deal_percent"] = mssg

    chosen_deal = context.user_data["chosen_deal"]
    leadgen_id = chosen_deal.leadgen_id
    leadgen = db_session.get_user(leadgen_id)
    leadgen_full_name = f"{leadgen.first_name} {leadgen.last_name}"
    linkedin = chosen_deal.linkedin
    deal_summ = context.user_data["deal_summ"]

    leadgen_get = round(int(deal_summ) / 100 * int(deal_percent))
    context.user_data["leadgen_get"] = leadgen_get

    reply_markup = [
        [text["yes"]],
        [text["cancel"]]
    ]

    markup = ReplyKeyboardMarkup(keyboard=reply_markup, resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat_id,
        text=text["deal_approve"].format(leadgen_full_name, linkedin, deal_summ, deal_percent, leadgen_get),
        reply_markup=markup
    )

    return States.DEAL_YES_APPROVE


def deal_yes_approve(update: Update, context: CallbackContext):
    
    chat_id = update.message.chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text=text["deal_yes_admin_thanks"],
    )

    chosen_deal = context.user_data["chosen_deal"]
    deal_summ = context.user_data["deal_summ"]
    deal_percent = context.user_data["deal_percent"]
    leadgen_get = context.user_data["leadgen_get"]
    # print(chosen_deal)
    db_session.deal_done(chosen_deal, leadgen_get)

    context.bot.send_message(
        chat_id=chosen_deal[2],
        text=text["deal_yes_lead_thanks"].format(leadgen_get),
    )
    context.user_data.pop("chosen_deal")
    context.user_data.pop("deal_summ")
    context.user_data.pop("deal_percent")
    context.user_data.pop("leadgen_get")
    return admin(update, context)