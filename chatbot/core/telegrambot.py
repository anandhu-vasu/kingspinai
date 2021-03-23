import importlib
import os

import telegram
from chatbot.core.chatbot import ChatBot
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher, Updater
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
        try:
            response = ChatBot(context.bot.token,telegram=True).reply(message)
            for message in response:
                context.bot.sendMessage(chat_id=update.message.chat_id, text=str(message))
        except:
            context.bot.sendMessage(chat_id=update.message.chat_id, text='You are Restricted...!')
            context.bot.sendMessage(chat_id=update.message.chat_id, text='Sorry for the Inconvenience')

def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    #dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot name

    bots = settings.DJANGO_TELEGRAMBOT['BOTS']

    for bot in bots:
        if bot["TOKEN"] != "1639137992:AAGNJ_-zOm5DwTMnx6zEEaTY9VoZCUFULUM":
            dp = DjangoTelegramBot.getDispatcher(bot["TOKEN"])     #get by bot token
            if dp:
                dp.add_handler(CommandHandler("start", start))
                dp.add_handler(CommandHandler("help", help))
                dp.add_handler(MessageHandler(Filters.text, reply))


