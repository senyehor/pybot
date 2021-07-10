import logging

from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from app import DISPATCHER
from bot_funcs import (
    inappropriate_answer_handler,
    ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS,
    WHOLE,
    get_activity_name_handler,
    get_activity_timings_handler,
    USER_CHOOSING_OPTIONS,
    plug,
    start_handler,
    user_choice_handler,
    keyboard_input_pattern,
    did_not_catch_regex
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG  # noqa
)
logger = logging.getLogger(__name__)

inappropriate_answer_handler = MessageHandler(Filters.all, inappropriate_answer_handler)
# if renaming check search in comments and strings
# and rename ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS in bot_funcs.py
ADD_ACTIVITY_SUBCONVERSATION = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, get_activity_name_handler)],  # noqa
    states={  # noqa
        ACTIVITY_ATTRIBUTES_OR_ADD_ACTIVITY_SUBCONVERSATION_OPTIONS.TIMINGS: [
            MessageHandler(Filters.regex(WHOLE), get_activity_timings_handler)
        ]
    },
    fallbacks=[inappropriate_answer_handler],  # noqa
    map_to_parent={
        ConversationHandler.END: USER_CHOOSING_OPTIONS.CHOOSE
    }
)

plug = MessageHandler(Filters.all, plug)

main_endless_conversation = ConversationHandler(
    entry_points=[CommandHandler('start', start_handler)],
    states={
        USER_CHOOSING_OPTIONS.CHOOSE: [
            MessageHandler(Filters.regex(keyboard_input_pattern), user_choice_handler),
            MessageHandler(Filters.all, did_not_catch_regex)
        ],
        USER_CHOOSING_OPTIONS.ADD: [
            plug
        ],
        USER_CHOOSING_OPTIONS.START: [
            plug
        ],
        USER_CHOOSING_OPTIONS.EDIT: [
            plug
        ],
        USER_CHOOSING_OPTIONS.DELETE: [
            plug
        ]
    },
    fallbacks=[inappropriate_answer_handler],  # noqa
    allow_reentry=True,
    name='main_endless_conversation'
)
DISPATCHER.add_handler(main_endless_conversation)
