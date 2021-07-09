import logging
import os

import flask
import telegram
from flask import Flask, request
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler

from bot_funcs import (
    inappropriate_answer_handler,
    ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS,
    WHOLE,
    get_activity_name_handler,
    get_activity_timings_handler,
    USER_CHOOSING_OPTIONS,
    tmp,
    start_handler,
    user_choice_handler,
    keyboard_iput_pattern
)

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG  # noqa
)
logger = logging.getLogger(__name__)

PORT = int(os.getenv('PORT'))
BOT_TOKEN = os.getenv('bot_token')
BOT_USERNAME = os.getenv('bot_username')
BOT_URL_PATH = os.getenv('bot_url_path')
BOT = telegram.Bot(BOT_TOKEN)
UPDATER = Updater(BOT_TOKEN, use_context=True)
DISPATCHER: Dispatcher = UPDATER.dispatcher

inappropriate_answer_handler = MessageHandler(Filters.all, inappropriate_answer_handler)
# if renaming check search in comments and strings
# and rename ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS in bot_funcs.py
ADD_ACTIVITY_SUBCONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, get_activity_name_handler)],  # noqa
    states={  # noqa
        ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.TIMINGS: [
            MessageHandler(Filters.regex(WHOLE), get_activity_timings_handler)
        ]
    },
    fallbacks=[inappropriate_answer_handler],  # noqa
    map_to_parent={
        ConversationHandler.END: USER_CHOOSING_OPTIONS.CHOOSING
    }
)

tmp = MessageHandler(Filters.all, tmp)

main_endless_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start_handler)],
    states={
        USER_CHOOSING_OPTIONS.CHOOSING: [
            MessageHandler(Filters.regex(keyboard_iput_pattern), user_choice_handler),
        ],
        USER_CHOOSING_OPTIONS.ADD: [
            tmp
        ],
        USER_CHOOSING_OPTIONS.START: [
            tmp
        ],
        USER_CHOOSING_OPTIONS.EDIT: [
            tmp
        ],
        USER_CHOOSING_OPTIONS.DELETE: [
            tmp
        ]
    },
    fallbacks=[inappropriate_answer_handler],  # noqa
    allow_reentry=True,

)
DISPATCHER.add_handler(main_endless_conversation)


@app.route(f'/{BOT_TOKEN}', methods=['POST', 'GET'])
def hooks_getter():
    """Bot sends hooks every time he gets a response and this func passes them to dispatcher"""
    try:
        update = telegram.Update.de_json(request.get_json(force=True), BOT)
        DISPATCHER.process_update(update)
    except:  # noqa
        return flask.Response(status=500)
    return flask.Response(status=200)


@app.route('/')
def index():
    return 'not sleeping'
