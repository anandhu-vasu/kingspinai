# import logging
# from telegram.ext import CommandHandler, MessageHandler, Filters
# from bots import KingspinAI
# from django_telegrambot.apps import DjangoTelegramBot

# # Enable logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )

# logger = logging.getLogger(__name__)



# def start(bot,update):
#     """Send a message when the command /start is issued."""
#     bot.sendMessage(update.message.chat_id, text='Hi!')
#     bot.sendMessage(update.message.chat_id, text="I'm a bot, created by kingspinai")
#     bot.sendMessage(update.message.chat_id, text="How may I help you?")


# def help(bot, update):
#     """Send a message when the command /help is issued."""
#     bot.sendMessage(update.message.chat_id, text='Help!')

# def reply(bot, update):
#     """send message"""
#     message = update.message.text

#     if message.lower() == 'bye':
#         bot.sendMessage(update.message.chat_id, text="Bye")

#     else:
#         response = KingspinAI.get_response(message)
#         if response.confidence == 0:
#             bot.sendMessage(update.message.chat_id, text="Sorry, I don't understand.")
#         else:
#             bot.sendMessage(update.message.chat_id, text=str(response))

# def error(bot, update, error):
#     logger.warn('Update "%s" caused error "%s"' % (update, error))

# def main():
#     logger.info("Loading handlers for telegram bot")

#     dispatcher = DjangoTelegramBot.dispatcher

#     dispatcher.add_handler(CommandHandler("start", start))
#     dispatcher.add_handler(CommandHandler("help", help))
#     dispatcher.add_handler(MessageHandler(Filters.text, reply))
#     dispatcher.add_error_handler(error)
    
# if __name__ == '__main__':
#     main()

#myapp/telegrambot.py
# Example code for telegrambot.py module
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from telegram import Bot,Update

import logging
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot:Bot, update:Update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


# def help(bot, update):
#     bot.sendMessage(update.message.chat_id, text='Help!')


# def echo(bot, update):
#     bot.sendMessage(update.message.chat_id, text=update.message.text)


# def error(bot, update, error):
#     logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    # dp.add_error_handler(error)