import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
from bots import KingspinAI
from django_telegrambot.apps import DjangoTelegramBot

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)



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

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    logger.info("Loading handlers for telegram bot")

    dispatcher = DjangoTelegramBot.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.text, reply))
    dispatcher.add_error_handler(error)
    
if __name__ == '__main__':
    main()