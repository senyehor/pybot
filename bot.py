import logging
import os
import flask
import requests
from flask import Flask, request
import telegram
from boto.s3.connection import S3Connection  # for accessing app`s config vars locally
from telegram import Update
from telegram.ext import Updater, CommandHandler, Dispatcher, CallbackContext
from pprint import pp

app = Flask(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG  # noqa
)
logger = logging.getLogger(__name__)

SET_WEBHOOK = False

PORT = int(os.getenv('PORT'))
BOT_TOKEN = os.getenv('bot_token')
BOT_USERNAME = os.getenv('bot_username')
BOT_URL_PATH = os.getenv('bot_url_path')
BOT = telegram.Bot(BOT_TOKEN)
UPDATER = Updater(BOT_TOKEN)
DISPATCHER: Dispatcher = UPDATER.dispatcher
index_debug_msg = 'not set up'


def pog(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('pog')


DISPATCHER.add_handler(CommandHandler('pog', pog))


# TODO: deal
# func to set up webhook
@app.before_first_request
def run_bot():
    if SET_WEBHOOK:
        UPDATER.start_webhook(listen='0.0.0.0',
                              port=PORT,
                              url_path=BOT_TOKEN,
                              webhook_url=BOT_URL_PATH + BOT_TOKEN)


# if __name__ == 'bot':
# run_bot()


@app.route(f'/{BOT_TOKEN}', methods=['POST', 'GET'])
def hooks_getter():
    """Bot sends hooks every time he gets a message and this func processes them"""
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    text = update.message.text.encode('utf-8').decode()
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    BOT.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=message_id)
    return flask.Response(status=200)


@app.route('/')
def index():
    for i in DISPATCHER.handlers:
        print(f'dispatcher {i}')
    return 'ok'


def dict_to_str(dict: dict):
    pp(dict)
    if dict == None:
        return 'Noneg'
    res = ''
    for key, value in dict.items():
        res += f'key : "{key}" || value : "{value}"\n'
    return res
