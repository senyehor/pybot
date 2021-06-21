import os
import requests
from flask import Flask, request
import telegram
from boto.s3.connection import S3Connection  # for accessing app`s config vars locally

BOT_TOKEN = os.getenv('bot_token')
BOT_USERNAME = os.getenv('bot_username')
BOT_URL_PATH = os.getenv('bot_url_path')
BOT = telegram.Bot(BOT_TOKEN)
bot_response_for_debug = 'not set up'

app = Flask(__name__)

#func to set up webhook
# @app.before_first_request
# def run_bot():
#     global bot_response_for_debug
#     _ = BOT.set_webhook(f'{BOT_URL_PATH}{BOT_TOKEN}')
#     if _:
#         bot_response_for_debug = 'webhook setup ok'
#     bot_response_for_debug = 'webhook setup failed'


def get_name():
    print(__name__)


# if __name__ == 'bot':
# run_bot()


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


@app.route('/')
def index():
    print('degugg')
    return dict_to_str(BOT.get_webhook_info().to_dict())


def dict_to_str(dict: dict):
    res = ''
    for key, value in dict.items():
        res += f'key : "{key}" || value : "{value}"\n'
    return res
