from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    print("------start")
    welcome_message = """Hi, this bot is developed to track your studying activity <3"""
    update.message.reply_text(text=welcome_message)
    # TODO : add inline kbrd
