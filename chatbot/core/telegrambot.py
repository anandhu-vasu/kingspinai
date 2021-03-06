from chatbot.core.chatbot import ChatBot
from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Hi!')
    context.bot.sendMessage(chat_id=update.message.chat_id, text='I\'m a bot, created using kingspinai')
    context.bot.sendMessage(chat_id=update.message.chat_id, text='How may I help you?')

def help(update, context):
    """send message"""
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Help!')

def reply(update, context):
    """send message"""
    message = update.message.text

    if message.lower() == 'bye':
        context.bot.sendMessage(chat_id=update.message.chat_id, text='Bye')
    else:
        response = ChatBot(context.bot.token,telegram=True).reply(message)
        context.bot.sendMessage(chat_id=update.message.chat_id, text=str(response))

def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    #dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot name
    for bot in settings.DJANGO_TELEGRAMBOT['BOTS']:

        dp = DjangoTelegramBot.getDispatcher(bot["TOKEN"])     #get by bot token

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))

        dp.add_handler(MessageHandler(Filters.text, reply))
