import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bots import KingspinAI
from django_telegrambot.apps import DjangoTelegramBot

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


PORT = int(os.environ.get('PORT', '8443'))
TOKEN = "1591577456:AAFoSp4IrLO0u293iRqyIQW0iOcd9Ml3OW0"
TEURL = "https://kingspin-ai.herokuapp.com/"


def start(bot,update):
    """Send a message when the command /start is issued."""
    bot.sendMessage(update.message.chat_id, text='Hi!')
    bot.sendMessage(update.message.chat_id, text="I'm a bot, created by kingspinai")
    bot.sendMessage(update.message.chat_id, text="How may I help you?")


def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.sendMessage(update.message.chat_id, text='Help!')

def reply(bot, update):
    """send message"""
    message = update.message.text

    if message.lower() == 'bye':
        bot.sendMessage(update.message.chat_id, text="Bye")

    else:
        response = KingspinAI.get_response(message)
        if response.confidence == 0:
            bot.sendMessage(update.message.chat_id, text="Sorry, I don't understand.")
        else:
            bot.sendMessage(update.message.chat_id, text=str(response))



def main():

    dispatcher = DjangoTelegramBot.dispatcher


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    reply_handler = MessageHandler(Filters.text, reply)
    dispatcher.add_handler(reply_handler)
    # updater.start_polling()

    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TOKEN)
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    # updater.bot.set_webhook(TEURL + TOKEN)
    # updater.start_polling()
    # updater.idle()
