from chatbot.core.chatbot import ChatBot

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