import logging

from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler

from bot_funcs import start, GENDER, PHOTO, LOCATION, photo, gender, skip_photo, location, skip_location, bio, BIO, \
    cancel

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],  # noqa
    states={  # noqa
        GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
        PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
        LOCATION: [
            MessageHandler(Filters.location, location),
            CommandHandler('skip', skip_location),
        ],
        BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],  # noqa
)
