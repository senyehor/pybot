from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    print("------start")
    welcome_message = """Hi, I`m developed to track your studying activity <3"""
    update.message.reply_text(text=welcome_message)
    # TODO : add inline kbrd


def non_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hmmm, I`m not really into chatting, im at work, you know')
