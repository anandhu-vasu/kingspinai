from chatbot.core.chatbot import BotType, ChatBot

def start(update, context):
    """Send a message when the command /start is issued."""
    name = update.message.chat.first_name+' '+ update.message.chat.last_name
    response = ChatBot.intro(context.bot.token,bot_type=BotType.TELEGRAM,uname=name)
    for message in response:
        context.bot.sendMessage(chat_id=update.message.chat_id, text=str(message))


def help(update, context):
    """send message"""
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Help!')

def reply(update, context):
    """send message"""
    message = update.message.text
    name = update.message.chat.first_name+' '+ update.message.chat.last_name

    try:
        response = ChatBot(context.bot.token,bot_type=BotType.TELEGRAM,uname=name).reply(message)
        for message in response:
            context.bot.sendMessage(chat_id=update.message.chat_id, text=str(message))
    except:
        context.bot.sendMessage(chat_id=update.message.chat_id, text='You are Restricted...!')
        context.bot.sendMessage(chat_id=update.message.chat_id, text='Sorry for the Inconvenience')