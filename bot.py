from flask import Flask, request
import telegram
from credentials_setup import get_value_from_dotenv

BOT_TOKEN = get_value_from_dotenv('bot_token')
BOT_USERNAME = get_value_from_dotenv('bot_username')
URL_BOT_PATH = get_value_from_dotenv('url_bot_path')
BOT = telegram.Bot(BOT_TOKEN)

app = Flask(__name__)


@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), BOT)
    text = update.message.text.encode('utf-8').decode()
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    if text == '/start':
        welcome_msg = """
        This bot is developed for tracking studying consistency and helps manage studying process 
        """
        BOT.sendMessage(chat_id=chat_id, text=welcome_msg, reply_to_message_id=message_id)


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    _ = BOT.set_webhook(f'{URL_BOT_PATH}{BOT_TOKEN}')
    if _:
        return 'webhook setup ok'
    return 'webhook setup failed'


@app.route('/')
def index():
    return '.'


def run_bot():
    app.run(threated=True)
