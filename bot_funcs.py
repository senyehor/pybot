from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def start_handler(update: Update, context: CallbackContext) -> None:
    print("------start")
    welcome_message = """Hi, I`m developed to track your studying activity <3"""
    update.message.reply_text(text=welcome_message, reply_markup=create_starting_choices_inline_kbrd_for_user('pass'))
    # TODO : add inline kbrd


def non_command_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hmmm, I`m not really into chatting, im at work, you know')


def create_starting_choices_inline_kbrd_for_user(username: str):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    keyboard = InlineKeyboardMarkup(keyboard)
    return keyboard


def starting_choices_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f'you selected {query.data}')
