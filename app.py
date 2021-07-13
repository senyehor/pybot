import logging
import os

import telegram
from flask import Flask, request, Response
from telegram.ext import Dispatcher, Updater

from bot import main_endless_conversation

app = Flask(__name__)

PORT = int(os.getenv('PORT'))
BOT_TOKEN = os.getenv('bot_token')
BOT_USERNAME = os.getenv('bot_username')
BOT_URL_PATH = os.getenv('bot_url_path')
BOT = telegram.Bot(BOT_TOKEN)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def setup_and_return_dispatcher():
    dispatcher = Dispatcher(BOT, None, workers=0)  # noqa
    dispatcher.add_handler(main_endless_conversation)
    return dispatcher


DISPATCHER = setup_and_return_dispatcher()
logger.debug(f'DISPATCHER with id {id(DISPATCHER)} was created')


@app.route(f'/{BOT_TOKEN}', methods=['POST', 'GET'])
def webhooks_getter():
    """Bot sends hooks every time he gets a message and this func passes them to dispatcher"""
    try:
        update = telegram.Update.de_json(request.get_json(force=True), BOT)
        DISPATCHER.process_update(update)
        logger.debug(f'dispatcher with id {id(DISPATCHER)} processed update')
    except:  # noqa
        return Response(status=500)
    return Response(status=200)


@app.route('/')
def index():
    return 'not sleeping'


def set_webhook():
    updater = Updater(BOT_TOKEN)
    updater.start_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=BOT_URL_PATH + BOT_URL_PATH
    )
