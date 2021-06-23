import logging
import os
import flask
from flask import Flask, request
import telegram
from telegram.ext import Updater, CommandHandler, Dispatcher, MessageHandler, Filters, CallbackQueryHandler
from pprint import pp
from bot_funcs import *

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
DISPATCHER = UPDATER.dispatcher

DISPATCHER.add_handler(CommandHandler('start', start_handler))
DISPATCHER.add_handler(MessageHandler(filters=Filters.text, callback=non_command_handler))
DISPATCHER.add_handler(CallbackQueryHandler(starting_choices_handler))


# func to set up webhook
@app.before_first_request
def run_bot():
    pass


@app.route(f'/{BOT_TOKEN}', methods=['POST', 'GET'])
def hooks_getter():
    """Bot sends hooks every time he gets a message and this func processes them"""
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    if request.method == 'POST':
        DISPATCHER.process_update(update)
        return flask.Response(status=200)
    text = update.message.text.encode('utf-8').decode()
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    if text.startswith('/'):
        pass
    BOT.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=message_id)
    return flask.Response(status=200)


@app.route('/')
def index():
    return 'ok'


def dict_to_str(dict: dict):
    pp(dict)
    res = ''
    for key, value in dict.items():
        res += f'key : "{key}" || value : "{value}"\n'
    return res
