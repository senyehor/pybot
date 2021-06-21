import errno
import os
import requests
from flask import Flask, request
import telegram
from boto.s3.connection import S3Connection  # for accessing app`s config vars locally
from telegram.ext import Updater
from pprint import pp

PORT = int(os.getenv('PORT'))
BOT_TOKEN = os.getenv('bot_token')
BOT_USERNAME = os.getenv('bot_username')
BOT_URL_PATH = os.getenv('bot_url_path')
BOT = telegram.Bot(BOT_TOKEN)
index_debug_msg = 'not set up'

app = Flask(__name__)


# TODO: deal
# func to set up webhook
@app.before_first_request
def run_bot():
    global bot_response_for_debug
    updater = Updater(BOT_TOKEN)
    pp(dict_to_str(BOT.get_webhook_info().to_dict()))
    # updater.start_webhook(listen='0.0.0.0',
    #                       port=PORT,
    #                       url_path=BOT_TOKEN,
    #                       webhook_url=BOT_URL_PATH + BOT_TOKEN)
    # updater.idle()


def get_name():
    print(__name__)


# if __name__ == 'bot':
# run_bot()


@app.route(f'/{BOT_TOKEN}', methods=['POST', 'GET'])
def hooks_getter():
    """Bot sends hooks every time he gets a message and this func processes them"""
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    text = update.message.text.encode('utf-8').decode()
    print(text)
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    if text == '/start':
        welcome_msg = """
        This bot is developed for tracking studying consistency and helps manage studying process 
        """
        BOT.sendMessage(chat_id=chat_id, text=welcome_msg, reply_to_message_id=message_id)


@app.route('/')
def index():
    return index_debug_msg


def dict_to_str(dict: dict):
    res = ''
    for key, value in dict.items():
        res += f'key : "{key}" || value : "{value}"\n'
    return res
