import os
from queue import Queue
from threading import Thread

import telegram
from flask import Flask, request, Response
from telegram.ext import Dispatcher

from bot import conv_handler

app = Flask(__name__)

PORT = int(os.getenv('PORT'))
BOT_TOKEN = os.getenv('bot_token')
BOT_USERNAME = os.getenv('bot_username')
BOT_URL_PATH = os.getenv('bot_url_path')
BOT = telegram.Bot(BOT_TOKEN)


def setup():
    update_queue = Queue()
    dispatcher = Dispatcher(BOT, update_queue)
    dispatcher.add_handler(conv_handler)
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    return update_queue


UPDATE_QUEUE = setup()


@app.route(f'/{BOT_TOKEN}', methods=['POST', 'GET'])
def webhooks_getter():
    """Bot sends hooks every time he gets a message and this func passes them to dispatcher"""
    try:
        update = telegram.Update.de_json(request.get_json(force=True), BOT)
        UPDATE_QUEUE.put(update)
    except:  # noqa
        return Response(status=500)
    return Response(status=200)


@app.route('/')
def index():
    return 'not sleeping'
