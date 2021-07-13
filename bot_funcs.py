import logging
from collections import namedtuple

from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup  # noqa
from telegram.ext import CallbackContext, ConversationHandler  # noqa

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)

USER_CHOOSING_OPTIONS = namedtuple(
    'Choices',
    ['CHOOSE', 'ADD', 'EDIT', 'DELETE', 'START', 'CANCEL']) \
    ('CHOOSE', 'ADD', 'EDIT', 'DELETE', 'START', 'CANCEL')
ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS = namedtuple(
    'Activity_attributes',
    ['NAME', 'TIMINGS']) \
    ('NAME', 'TIMINGS')
OPTIONS_MESSAGES = {
    USER_CHOOSING_OPTIONS.CHOOSE: 'Choose what to do',
    USER_CHOOSING_OPTIONS.ADD: 'Enter name of activity',
    USER_CHOOSING_OPTIONS.EDIT: 'What activity you want to edit?',
    USER_CHOOSING_OPTIONS.DELETE: 'Choose activity to delete',
    USER_CHOOSING_OPTIONS.START: 'Choose activity to start',
    USER_CHOOSING_OPTIONS.CANCEL: 'Backing',
    ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.TIMINGS:
        'Enter how many days per week you want to practice and time you want to practice with breaks, whitespaces '
        'ignored, except at the end (do not place spaces at the end. Example 5,1:15;15;1:15;15;1:15 means you want to'
        ' practice 5 times per week, 1:15h 3 times with 15m breaks'
}
days_and_comma = r'\s*\d\s*,'
time = r'\s*((\d:\d\d)|(\d\d)|(\d))'
WHOLE = days_and_comma + fr'({time};)*' + time + '$'
start_words = ''
for word in USER_CHOOSING_OPTIONS._fields:
    word = word.capitalize()
    start_words += f'({word})'
    if word != USER_CHOOSING_OPTIONS._fields[-1].capitalize():
        start_words += '|'
keyboard_input_pattern = f'^({start_words})'

CONVERSATION_STATE = 'CONVERSATION_STATE'


def send_message(text: str, context: CallbackContext, reply_markup: InlineKeyboardMarkup = None):
    context.bot.send_message(text=text, chat_id=_get_chat_id(context), reply_markup=reply_markup)


def _get_state(context: CallbackContext):
    return context.user_data.get(CONVERSATION_STATE, None)


def _set_state(state: str, context: CallbackContext):
    send_message(f'_set from {_get_state(context)} to {state}', context)
    context.user_data[CONVERSATION_STATE] = state


def log(func):
    def wrap(*args, **kwargs):
        _, context = args
        state_at_start = _get_state(context)
        result = func(*args, **kwargs)
        state_at_end = _get_state(context)
        logger.debug(f'\n@log func {func.__name__} from {state_at_start} --> {state_at_end}\n')
        return result

    return wrap


def _get_chat_id(context: CallbackContext):
    return context.user_data['CHAT_ID']


def _set_chat_id(chat_id, context: CallbackContext):
    context.user_data['CHAT_ID'] = chat_id


def start(update: Update, context: CallbackContext):
    _set_chat_id(update.message.chat_id, context)
    send_message('Hi, its a test start msg)', context, create_starting_choices_inline_keyboard('plug'))
    return USER_CHOOSING_OPTIONS.CHOOSE


def create_starting_choices_inline_keyboard(username: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("Add new activity, tracker", callback_data=USER_CHOOSING_OPTIONS.ADD)],
        [InlineKeyboardButton("Start activity", callback_data=USER_CHOOSING_OPTIONS.START)],
        [InlineKeyboardButton("Edit activity", callback_data=USER_CHOOSING_OPTIONS.EDIT)],
        [InlineKeyboardButton("Delete activity", callback_data=USER_CHOOSING_OPTIONS.DELETE)]
    ]
    buttons = InlineKeyboardMarkup(buttons)
    return buttons
