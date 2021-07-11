import os

import telegram
from flask import Flask, request, Response
from telegram.ext import Dispatcher

from bot import main_endless_conversation

app = Flask(__name__)

PORT = int(os.getenv('PORT'))
BOT_TOKEN = os.getenv('bot_token')
BOT_USERNAME = os.getenv('bot_username')
BOT_URL_PATH = os.getenv('bot_url_path')
BOT = telegram.Bot(BOT_TOKEN)
DISPATCHER = Dispatcher(BOT, None, workers=0)  # noqa
if not DISPATCHER.handlers:
    DISPATCHER.add_handler(main_endless_conversation)


@app.route(f'/{BOT_TOKEN}', methods=['POST', 'GET'])
def webhooks_getter():
    """Bot sends hooks every time he gets a message and this func passes them to dispatcher"""
    try:
        update = telegram.Update.de_json(request.get_json(force=True), BOT)
        DISPATCHER.process_update(update)
    except:  # noqa
        return Response(status=500)
    return Response(status=200)


@app.route('/')
def index():
    return 'not sleeping'
