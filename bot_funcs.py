import logging
from collections import namedtuple

from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton  # noqa
from telegram.ext import CallbackContext, ConversationHandler  # noqa

from custom_google_classes import Activity, ActivitiesManager

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


def send_message(text: str, context: CallbackContext, reply_markup: ReplyKeyboardMarkup = None):
    context.bot.send_message(text=text, chat_id=_get_chat_id(context), reply_markup=reply_markup)


def _get_state(context: CallbackContext):
    return context.user_data[CONVERSATION_STATE]


def _set_state(state: str, context: CallbackContext):
    send_message(f'_set from {_get_state(context)} to {state}', context)
    context.user_data[CONVERSATION_STATE] = state


def log(func):
    def wrap(*args, **kwargs):
        _, context = args
        if func.__name__ == 'start_handler':  # todo del
            context.user_data[CONVERSATION_STATE] = 'START'
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


@log
def send_message_by_state(state: str, context: CallbackContext):
    """State should be an attribute of defined ..._OPTIONS namedtuple"""
    send_message(OPTIONS_MESSAGES[state], context)


@log
def set_next_conversation_state_send_message_by_state_and_return_state(state: str, context: CallbackContext) -> str:
    """State should be an attribute of defined ..._OPTIONS namedtuple"""
    logger.debug(f'@log from {_get_state(context)} --> {state}')
    _set_state(state, context)
    send_message_by_state(state, context)
    return state


@log
def plug(update: Update, context: CallbackContext):
    logger.debug(f'@log tmp - current state is {_get_state(context)}')
    return set_next_conversation_state_send_message_by_state_and_return_state(USER_CHOOSING_OPTIONS.CHOOSE, context)


def did_not_catch_regex(update: Update, context: CallbackContext):
    send_message('did not catch', context)


@log
def user_choice_handler(update: Update, context: CallbackContext):
    try:
        user_choice = update.message.text.split(' ')[0].upper()
        send_message(user_choice, context)
    except:
        logger.debug('Exept happend')
        return inappropriate_answer_handler(update, context)
    result = user_choice not in USER_CHOOSING_OPTIONS._fields
    if result:
        logger.debug(f'{user_choice} not in fields')
        return inappropriate_answer_handler(update, context)
    logger.debug(f'state {user_choice} in fields')
    logger.debug(f'went to set_... with state {user_choice}')
    return set_next_conversation_state_send_message_by_state_and_return_state(user_choice, context)


@log
def start_handler(update: Update, context: CallbackContext) -> USER_CHOOSING_OPTIONS.ADD:
    """First thing user will do is add an activity, so after /start user goes into ADD_ACTIVITY_SUBCONVERSATION"""
    _set_chat_id(update.message.chat_id, context)
    send_message('Hi, I`m developed to track your studying activity <3, lets get started and add an activity.',
                 context,
                 create_starting_choices_inline_keyboard(''))
    return set_next_conversation_state_send_message_by_state_and_return_state(USER_CHOOSING_OPTIONS.CHOOSE, context)


def create_starting_choices_inline_keyboard(username: str) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton("Add new activity tracker")],
        [KeyboardButton("Start activity")],
        [KeyboardButton("Edit activity")],
        [KeyboardButton("Delete activity")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    return keyboard


@log
def inappropriate_answer_handler(update: Update, context: CallbackContext):
    state = _get_state(context)
    send_message(f'Got an unexpected reply with state {state}', context)
    return set_next_conversation_state_send_message_by_state_and_return_state(state, context)


def cancel_handler(update: Update, context: CallbackContext):
    return USER_CHOOSING_OPTIONS.CANCEL


@log
def get_activity_name_handler(update: Update, context: CallbackContext):
    # todo add check if user already has activity with same name
    # todo think of setting conv state one approach
    _set_state(ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.NAME, context)
    context.user_data[ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.NAME] = update.message.text
    return set_next_conversation_state_send_message_by_state_and_return_state(
        ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.TIMINGS, context)


@log
def get_activity_timings_handler(update: Update, context: CallbackContext):
    timings_from_user = update.message.text.replace(' ', '').replace(',', '|')  # format properly to how its stored
    activity_name = context.user_data.get(ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.NAME)
    # add_activity(update.effective_user.username, activity_name, timings_from_user)
    send_message(f'{timings_from_user = } {activity_name = }', context)
    send_message('Activity was successfully added', context)
    return ConversationHandler.END


def add_activity(username: str, activity_name: str, timings: str):
    manager = ActivitiesManager.get_activities_manager(username)
    activity = Activity(username, activity_name, timings)
    manager.add_activity(activity)
    return ConversationHandler.END


def start_activity(username: str, activity_name: str):
    pass


def edit_activity(username: str, activity_name: str):
    pass


def delete_activity(username: str, activity_name: str):
    pass
