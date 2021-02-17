import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bots import KingspinAI

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


PORT = int(os.environ.get('PORT', '8443'))
TOKEN = "1591577456:AAFoSp4IrLO0u293iRqyIQW0iOcd9Ml3OW0"
TEURL = "https://kingspin-ai.herokuapp.com/tehook/"


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("I'm a bot, created by kingspinai")
    update.message.reply_text("how may i help you ?")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')



def reply(update: Update, context: CallbackContext) -> None:
    """send message"""
    message = update.message.text

    if message == 'Bye':
        update.message.reply_text("bye")

    else:
        response = KingspinAI.get_response(message)
        if response.confidence == 0:
            update.message.reply_text("i don't understand")
        else:
            update.message.reply_text(text=str(response))



def main():

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    reply_handler = MessageHandler(Filters.text, reply)
    dispatcher.add_handler(reply_handler)
    # updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    updater.bot.set_webhook(TEURL + TOKEN)
    
    updater.idle()


if __name__ == '__main__':
    main()