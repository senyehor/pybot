import logging
import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from collections import namedtuple
import asyncio

USER_ACTIONS_OPTIONS = namedtuple('Choices', ['ADD', 'START', 'EDIT', 'DELETE'])('ADD', 'START', 'EDIT', 'DELETE')


def start_handler(update: Update, context: CallbackContext) -> None:
    print("------start")
    welcome_message = """Hi, I`m developed to track your studying activity <3"""
    update.message.reply_text(text=welcome_message, reply_markup=create_starting_choices_inline_kbrd_for_user('pass'))
    # TODO : add inline kbrd


def non_command_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hmmm, I`m not really into chatting, im at work, you know')


def create_starting_choices_inline_kbrd_for_user(username: str):
    keyboard = [
        [InlineKeyboardButton("Add new activity tracker", callback_data=USER_ACTIONS_OPTIONS.ADD)],
        [InlineKeyboardButton("Start activity", callback_data=USER_ACTIONS_OPTIONS.START)],
        # TODO : add user options
        [InlineKeyboardButton("Edit activity", callback_data=USER_ACTIONS_OPTIONS.EDIT)],
        [InlineKeyboardButton("Delete activity", callback_data=USER_ACTIONS_OPTIONS.DELETE)]
    ]

    keyboard = InlineKeyboardMarkup(keyboard)
    return keyboard


def starting_choices_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f'you selected {query.data}')


def set_timer_handler(update: Update, context: CallbackContext):
    logger = logging.getLogger()
    logger.debug('Entered set_timer')
    time.sleep(50)
    update.message.reply_text('10 sec has gone')


async def async_timer() -> None:
    await asyncio.sleep(10)
