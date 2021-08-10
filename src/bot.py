""" main finction to launch bot """
import os
import sys
from datetime import time as datetime_time
from datetime import timedelta
import logging # used for error detection

from dotenv import load_dotenv
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import PicklePersistence
from telegram.ext import Updater
from telegram.utils.request import Request

from .data import TIME_ZONE
from .data import TIMER_RANGE
from .data import text
from .states import States
from .hanlders import start
from .hanlders import password_check
from .hanlders import admin
from .hanlders import pick_call
from .hanlders import call_feedback
from .hanlders import call_yes
from .hanlders import call_no
from .hanlders import send_description
from .hanlders import get_stats
from .hanlders import plan_call
from .hanlders import call_plan_date
from .hanlders import call_plan_time
from .hanlders import call_plan_link
# from .handlers import timed_mailing
# from .utils import cached_data

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

print("-------- succesful import --------")


def done(update, context):
    # context.bot.send_message('Your message was not recognized')
    return ConversationHandler.END


def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """ inicialise handlers and start the bot """

    # storage_file = "storage"
    # my_persistence = PicklePersistence(filename=storage_file)
    
    bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
    updater = Updater(token=bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # crone jobs
    # ==========

    # j = updater.job_queue

    # callback_time = datetime_time(hour=7, tzinfo=TIME_ZONE)
    # j.run_daily(callback=everyday_ask_work, time=callback_time)

    # j.run_repeating(callback=timed_mailing, interval=60, first=1)

    # for hour in range(TIMER_RANGE[0], TIMER_RANGE[1] + 1):
    #     callback_time = datetime_time(hour=hour, tzinfo=TIME_ZONE)
    #     j.run_daily(callback=timed_mailing, time=callback_time)

    # massage handlers
    # ================

    necessary_handlers = [CommandHandler('start', start),
                          CommandHandler('stop', done),
                          CommandHandler('admin', admin)]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            ## user
            States.PASSWORD_CHECK: [
                *necessary_handlers,
                MessageHandler(Filters.text, password_check)],


            ## admin
            States.ADMIN_MENU: [
                *necessary_handlers,
                MessageHandler(Filters.text(text["mssg_call"]), pick_call),
                MessageHandler(Filters.text(text["get_stats"]), get_stats)],
            
            States.ADMIN_CALL_CHOSEN: [
                *necessary_handlers,
                MessageHandler(Filters.text, call_feedback)],
            
            States.HAS_CALL_BEEN: [
                *necessary_handlers,
                MessageHandler(Filters.text(text["yes"]), call_yes),
                MessageHandler(Filters.text(text["no"]), call_no)],
            
            States.CALL_NO_DESCRIPTION: [
                *necessary_handlers,
                MessageHandler(Filters.text, send_description)],


            ## leadgen
            States.CALL_PLAN_DATE: [
                *necessary_handlers,
                MessageHandler(Filters.text, call_plan_date)],
            
            States.CALL_PLAN_TIME: [
                *necessary_handlers,
                MessageHandler(Filters.text, call_plan_time)],
            
            States.CALL_PLAN_LINK: [
                *necessary_handlers,
                MessageHandler(Filters.text, call_plan_link)],
        },

        fallbacks=[CommandHandler('stop', done)], allow_reentry=True
    )

    dispatcher.add_handler(conv_handler)
    # dispatcher.add_handler(CommandHandler("info", info))

    dispatcher.add_handler(CommandHandler("call", plan_call))

    dispatcher.add_error_handler(error_handler)

    if ("--web-hook" in sys.argv) or ("-w" in sys.argv):
        print("-------- starting webhook --------")
    #     host_port = int(os.getenv("WEBHOOK_PORT"))
    #     host_url = os.getenv("WEBHOOK_URL")
    #     webhook_host_url = f"https://{host_url}:{host_port}/{bot_token}"
    #     print("started on\n\n" + webhook_host_url)
    #     updater.start_webhook(
    #         listen="0.0.0.0",
    #         port=host_port,
    #         url_path=bot_token,
    #         key="private.key",
    #         cert="cert.pem",
    #         webhook_url=webhook_host_url,
    #     )
    else:
        print("-------- starting polling --------")
        updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
