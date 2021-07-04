import os
from pprint import pp
from collections import namedtuple
from typing import Union

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup  # noqa
from telegram.ext import CallbackContext  # noqa

from custom_google_classes import get_activities_manager, Activity, Spreadsheet

USER_ACTIONS_OPTIONS = namedtuple('Choices', ['ADD', 'START', 'EDIT', 'DELETE'])('ADD', 'START', 'EDIT', 'DELETE')


def start_handler(update: Update, context: CallbackContext) -> None:
    welcome_message = 'Hi, I`m developed to track your studying activity <3, lets get started and add an activity'
    keyboard = [['1', '2', '3']]
    update.message.reply_text(text=welcome_message,
                              reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    print('---------------userdata-------------------')
    pp(context.user_data)


def non_command_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hmm, I`m not really into chatting, im at work, you know')


def create_starting_choices_inline_keyboard(username: str) -> InlineKeyboardMarkup:
    user_activities_keyboard = create_users_activities_keyboard_with_purpose(username)
    keyboard = [
        [InlineKeyboardButton("Add new activity tracker", callback_data=USER_ACTIONS_OPTIONS.ADD)]
    ]
    if user_activities_keyboard:
        keyboard.extend([[InlineKeyboardButton("Start activity", callback_data=USER_ACTIONS_OPTIONS.START)],
                         [InlineKeyboardButton("Edit activity", callback_data=USER_ACTIONS_OPTIONS.EDIT)],
                         [InlineKeyboardButton("Delete activity", callback_data=USER_ACTIONS_OPTIONS.DELETE)]])
    keyboard = InlineKeyboardMarkup(keyboard)
    return keyboard


def create_users_activities_keyboard_with_purpose(username: str, purpose: str = '') \
        -> Union[InlineKeyboardMarkup, None]:
    keyboard = []
    activities_names_list: list[str] = get_activities_manager(username).get_activities_names_list()
    for activity_name in activities_names_list:
        keyboard += [InlineKeyboardButton(activity_name.capitalize(), callback_data=activity_name + ';' + purpose)]
    if keyboard:
        return InlineKeyboardMarkup(keyboard)
    return None


def create_activity(update: Update):
    username = update.effective_user.username
    new_activity = Activity(Spreadsheet(os.getenv('workbook_id'), ))


def main_manager(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    username = update.effective_user.username
    choice = query.data
    if choice in USER_ACTIONS_OPTIONS._fields:
        if choice == USER_ACTIONS_OPTIONS.ADD:
            create_activity(update)
            return
        update.message.reply_text('Choose activity',
                                  reply_markup=create_users_activities_keyboard_with_purpose(username, choice)
                                  )
    else:
        activity_name, action = choice.split(';')


def start_activity(username: str, activity_name: str):
    pass


def edit_activity(username: str, activity_name: str):
    pass


def delete_activity(username: str, activity_name: str):
    pass
