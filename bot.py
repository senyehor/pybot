import os
from multiprocessing import get_all_start_methods

import requests
from flask import Flask, request
import telegram
from boto.s3.connection import S3Connection  # for accessing app`s config vars locally

BOT_TOKEN = os.getenv('bot_token')
BOT_USERNAME = os.getenv('bot_username')
BOT_URL_PATH = os.getenv('bot_url_path')
BOT = telegram.Bot(BOT_TOKEN)

app = Flask(__name__)
bot_response_for_debug = None


@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def hooks_getter():
    """Bot sends hooks every time he gets a message"""
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    text = update.message.text.encode('utf-8').decode()
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    if text == '/start':
        welcome_msg = """
        This bot is developed for tracking studying consistency and helps manage studying process 
        """
        BOT.sendMessage(chat_id=chat_id, text=welcome_msg, reply_to_message_id=message_id)


@app.route(f'/{BOT_TOKEN}/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    _ = BOT.set_webhook(f'{BOT_URL_PATH}{BOT_TOKEN}')
    if _:
        return 'webhook setup ok'
    return 'webhook setup failed'


@app.route('/')
def index():
    return bot_response_for_debug


def run_bot():
    app.run(threated=True)
    global bot_response_for_debug
    bot_response_for_debug = requests.get(f'{BOT_URL_PATH}{BOT_TOKEN}/setwebhook') # set bot to send webhooks
    # TODO: Change from json to eatable