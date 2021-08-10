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