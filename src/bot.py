""" main finction to launch bot """
import os
import sys
from datetime import time as datetime_time
import logging

from dotenv import load_dotenv
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import PicklePersistence
from telegram.ext import Updater

from .data import TIME_ZONE
from .data import text
from .states import States
from .hanlders import start
from .hanlders import echo_service
from .hanlders import password_check
from .hanlders import everyday_ask_work
from .hanlders import everyday_create_stat
from .hanlders import everyday_check_who_answered
from .hanlders import del_user
from .hanlders import del_user_save
from .hanlders import push_mssg
from .hanlders import push_mssg_text
from .hanlders import push_mssg_final
from .hanlders import main_menu
from .hanlders import make_admin
from .hanlders import make_admin_role
from .hanlders import make_admin_save
from .hanlders import name
from .hanlders import report
from .hanlders import report_options
from .hanlders import change_connects_want
from .hanlders import change_connects
from .hanlders import connects
from .hanlders import admin
from .hanlders import pick_call
from .hanlders import call_feedback
from .hanlders import call_yes
from .hanlders import call_no
from .hanlders import send_description
from .hanlders import get_stats
from .hanlders import plan_call
from .hanlders import plan_call_date
from .hanlders import plan_call_time
from .hanlders import plan_call_link
from .hanlders import show_stats

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

print("-------- succesful import --------")


def done(update, context):
    return ConversationHandler.END


def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """ inicialise handlers and start the bot """

    storage_file = "storage"
    my_persistence = PicklePersistence(filename=storage_file)
    
    bot_token = os.getenv("BOT_TOKEN")  # variable, because it is neaded on webhook
    updater = Updater(token=bot_token, use_context=True, persistence=my_persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    if ("--service" in sys.argv) or ("-s" in sys.argv):
        print("!!!!!!!! bot on service !!!!!!!!")
        dispatcher.add_handler(MessageHandler((Filters.text | Filters.command), echo_service))
    else:
        # crone jobs
        # ==========

        j = updater.job_queue

        callback_time = datetime_time(hour=21, minute=00, tzinfo=TIME_ZONE)
        j.run_daily(callback=everyday_ask_work, time=callback_time)

        callback_time = datetime_time(hour=0, minute=4, tzinfo=TIME_ZONE)
        j.run_daily(callback=everyday_create_stat, time=callback_time)

        callback_time = datetime_time(hour=0, minute=2, tzinfo=TIME_ZONE)
        j.run_daily(callback=everyday_check_who_answered, time=callback_time)

        # massage handlers
        # ================

        necessary_handlers = [CommandHandler('start', start),
                            CommandHandler('stop', done),
                            CommandHandler('admin', admin),
                            CommandHandler('call', plan_call),
                            CommandHandler('report', report)
                            ]

        conv_handler = ConversationHandler(
            name="conversation",
            persistent=True,
            entry_points=[CommandHandler('start', start)],

            states={
                ## user
                States.PASSWORD_CHECK: [
                    CommandHandler('start', start),
                    CommandHandler('stop', done),
                    MessageHandler(Filters.text, password_check)],

                States.MAIN_MENU: [
                    *necessary_handlers,
                    MessageHandler(Filters.text, main_menu)],
                

                ## leadgen's reports
                States.NAME_AND_SURNAME: [
                    *necessary_handlers,
                    MessageHandler(Filters.text, name)],
                
                States.REPORT: [
                    *necessary_handlers,
                    MessageHandler(Filters.text, report_options)],

                States.CONNECTS: [
                    *necessary_handlers,
                    MessageHandler(Filters.text, connects)],

                States.CHANGE_CONNECTS_WANT: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["yes"]), change_connects_want),
                    MessageHandler(Filters.text(text["no"]), main_menu)
                ],

                States.CHANGE_CONNECTS: [
                    *necessary_handlers,
                    MessageHandler(Filters.text, change_connects)],


                ## admin
                States.ADMIN_MENU: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["back"]), main_menu),
                    MessageHandler(Filters.text(text["mssg_call"]), pick_call),
                    MessageHandler(Filters.text(text["get_stats"]), get_stats),
                    MessageHandler(Filters.text(text["make_admin"]), make_admin),
                    MessageHandler(Filters.text(text["del_user"]), del_user),
                    MessageHandler(Filters.text(text["push_mssg"]), push_mssg),
                ],
                
                States.ADMIN_CALL_CHOSEN: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["back"]), admin),
                    MessageHandler(Filters.text, call_feedback)],
                
                States.HAS_CALL_BEEN: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["yes"]), call_yes),
                    MessageHandler(Filters.text(text["no"]), call_no)],
                
                States.CALL_NO_DESCRIPTION: [
                    *necessary_handlers,
                    MessageHandler(Filters.text, send_description)],

                States.STATS_MENU: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["back"]), admin),
                    MessageHandler(Filters.text, show_stats)
                ],
                States.MAKE_ADMIN: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["back"]), admin),
                    MessageHandler(Filters.text, make_admin_role)
                ],
                States.MAKE_ADMIN_SAVE: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["back"]), admin),
                    MessageHandler(Filters.text, make_admin_save)
                ],
                States.DEL_USER: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["back"]), admin),
                    MessageHandler(Filters.text, del_user_save)
                ],
                States.PUSH_MSSG: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["back"]), admin),
                    MessageHandler(Filters.text, push_mssg_text)
                ],
                States.PUSH_MSSG_FINAL: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["cancel"]), admin),
                    MessageHandler(Filters.text, push_mssg_final)
                ],


                ## leadgen calls
                States.CALL_PLAN_DATE: [
                    *necessary_handlers,
                    MessageHandler(Filters.text(text["back"]), main_menu),
                    MessageHandler(Filters.text, plan_call_date)],
                
                States.CALL_PLAN_TIME: [
                    *necessary_handlers,
                    MessageHandler(Filters.text, plan_call_time)],
                
                States.CALL_PLAN_LINK: [
                    *necessary_handlers,
                    MessageHandler(Filters.text, plan_call_link)],
            },

            fallbacks=[CommandHandler('stop', done)], allow_reentry=True
        )

        dispatcher.add_handler(conv_handler)

    dispatcher.add_error_handler(error_handler)

    if ("--web-hook" in sys.argv) or ("-w" in sys.argv):
        print("-------- starting webhook --------")
        host_port = int(os.getenv("WEBHOOK_PORT"))
        host_url = os.getenv("WEBHOOK_URL")
        webhook_host_url = f"https://{host_url}:{host_port}/{bot_token}"
        print("started on\n\n" + webhook_host_url)
        updater.start_webhook(
            listen="0.0.0.0",
            port=host_port,
            url_path=bot_token,
            key="private.key",
            cert="cert.pem",
            webhook_url=webhook_host_url,
        )
    else:
        print("-------- starting polling --------")
        updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
