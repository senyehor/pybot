import logging

import flask
import telegram
from flask import Flask, request
from telegram.ext import Updater, Dispatcher, ConversationHandler, CommandHandler

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
DISPATCHER: Dispatcher = UPDATER.dispatcher

# conversation = ConversationHandler(
#     entry_points=[CommandHandler('start', start_handler)]
# )
DISPATCHER.add_handler(CommandHandler('test', start_handler))


# func to set up webhook
@app.before_first_request
def run_bot():
    pass


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


@app.route('/test_timer')
async def timer():
    await async_timer()
    return 'works'
