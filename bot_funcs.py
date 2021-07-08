import logging
from collections import namedtuple

from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton  # noqa
from telegram.ext import CallbackContext, ConversationHandler  # noqa

from custom_google_classes import Activity, ActivitiesManager

logger = logging.getLogger(__name__)

USER_CHOOSING_OPTIONS = namedtuple(
    'Choices',
    ['CHOOSING', 'ADD', 'EDIT', 'DELETE', 'START', 'CANCEL']) \
    ('CHOOSING', 'ADD', 'EDIT', 'DELETE', 'START', 'CANCEL')
ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS = namedtuple(
    'Activity_attributes',
    ['NAME', 'TIMINGS']) \
    ('NAME', 'TIMINGS')
OPTIONS_MESSAGES = {
    USER_CHOOSING_OPTIONS.CHOOSING: 'Choose what to do',
    USER_CHOOSING_OPTIONS.ADD: 'Enter name of activity',
    USER_CHOOSING_OPTIONS.EDIT: 'What activity you want to edit?',
    USER_CHOOSING_OPTIONS.DELETE: 'Choose activity to delete',
    USER_CHOOSING_OPTIONS.CANCEL: 'Backing',
    ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.TIMINGS:
        'Enter how many days per week you want to practice and time you want to practice with breaks, whitespaces '
        'ignored, except at the end (do not place spaces at the end. Example 5,1:15;15;1:15;15;1:15 means you want to'
        ' practice 5 times per week, 1:15h 3 times with 15m breaks'
}
days_and_comma = r'\s*\d\s*,'
time = r'\s*((\d:\d\d)|(\d\d)|(\d))'
whole = days_and_comma + fr'({time};)*' + time + '$'

CONVERSATION_STATE = 'CONVERSATION_STATE'


def log_output(func):
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.debug(f'{func.__name__} returned {result} ----------------------')
        return result

    return wrap


def log(func):
    def wrap(*args, **kwargs):
        logger.debug(f'Entered {func.__name__}' + '-' * 60)
        result = func(*args, **kwargs)
        logger.debug(f'Exited {func.__name__}' + '-' * 60)
        return result

    return wrap


def get_chat_id(context: CallbackContext):
    return context.user_data['CHAT_ID']


def set_chat_id(chat_id, context: CallbackContext):
    context.user_data['CHAT_ID'] = chat_id


@log
def tmp(update: Update, context: CallbackContext):
    context.bot.send_message(text='poh', chat_id=update.message.chat_id)
    return USER_CHOOSING_OPTIONS.CHOOSING


@log
def send_message_by_state(context: CallbackContext, state: str):
    """State should be an attribute of defined ..._OPTIONS namedtuple"""
    context.bot.send_message(text=OPTIONS_MESSAGES[state], chat_id=get_chat_id(context))


@log
def set_next_conversation_state_send_message_by_state_and_return_state(context: CallbackContext, state: str) -> str:
    """State should be an attribute of defined ..._OPTIONS namedtuple"""
    context.user_data[CONVERSATION_STATE] = state
    send_message_by_state(context, state)
    return state


@log
def get_activity_name_handler(update: Update, context: CallbackContext):
    # todo add check if user already has activity with same name
    # todo think of setting conv state one approach
    context.user_data[CONVERSATION_STATE] = ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.NAME
    context.user_data[ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.NAME] = update.message.text
    return set_next_conversation_state_send_message_by_state_and_return_state(
        context,
        ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.TIMINGS)


@log
def get_activity_timings_handler(update: Update, context: CallbackContext):
    timings_from_user = update.message.text.replace(' ', '').replace(',', '|')  # format properly to how its stored
    activity_name = context.user_data.get(ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.NAME)
    # add_activity(update.effective_user.username, activity_name, timings_from_user)
    context.bot.send_message(chat_id=get_chat_id(context), text=f'{timings_from_user = } {activity_name = }')
    context.bot.send_message(chat_id=get_chat_id(context), text='Activity was successfully added')
    return ConversationHandler.END


@log
def add_activity(username: str, activity_name: str, timings: str):
    manager = ActivitiesManager.get_activities_manager(username)
    activity = Activity(username, activity_name, timings)
    manager.add_activity(activity)
    return ConversationHandler.END


@log
def user_choice_handler(update: Update, context: CallbackContext):
    user_choice = update.message.text.upper()
    if user_choice not in USER_CHOOSING_OPTIONS._fields:
        inappropriate_answer_handler(update, context)
    return set_next_conversation_state_send_message_by_state_and_return_state(context, user_choice)


@log
def start_handler(update: Update, context: CallbackContext) -> USER_CHOOSING_OPTIONS.ADD:
    """First thing user will do is add an activity, so after /start user goes into ADD_ACTIVITY_SUBCONVERSATION"""
    context.bot.send_message(
        text='Hi, I`m developed to track your studying activity <3, lets get started and add an activity.',
        chat_id=update.message.chat_id)
    set_chat_id(update.message.chat_id, context)
    return set_next_conversation_state_send_message_by_state_and_return_state(context, USER_CHOOSING_OPTIONS.ADD)


@log
def inappropriate_answer_handler(update: Update, context: CallbackContext):
    state = context.user_data.get(CONVERSATION_STATE)
    context.bot.send_message(chat_id=get_chat_id(context), text='Got an unexpected reply')
    send_message_by_state(context, state)
    return state


def cancel_handler(update: Update, context: CallbackContext):
    return USER_CHOOSING_OPTIONS.CANCEL


def create_starting_choices_inline_keyboard(username: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton("Add new activity tracker", callback_data=USER_CHOOSING_OPTIONS.ADD)]
    ]
    # if user_activities_keyboard:
    #     keyboard.extend([[InlineKeyboardButton("Start activity", callback_data=USER_CHOOSING_OPTIONS.START)],
    #                      [InlineKeyboardButton("Edit activity", callback_data=USER_CHOOSING_OPTIONS.EDIT)],
    #                      [InlineKeyboardButton("Delete activity", callback_data=USER_CHOOSING_OPTIONS.DELETE)]])
    keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    return keyboard


def start_activity(username: str, activity_name: str):
    pass


def edit_activity(username: str, activity_name: str):
    pass


def delete_activity(username: str, activity_name: str):
    pass
