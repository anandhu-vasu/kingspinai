from chatbot.core.chatbot import Channel, ChatBot

def start(update, context):
    """Send a message when the command /start is issued."""

    def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
        return text.split()[1] if len(text.split()) > 1 else ''
    uid = extract_unique_code(update.message.text)
    auth = {"telegram":update.message.chat_id}
    uname = update.message.chat.first_name if update.message.chat.first_name else ''+' '+ update.message.chat.last_name if update.message.chat.last_name else ''
    response = ChatBot.intro(context.bot.token,channel=Channel.Telegram,uid=uid,uname=uname,auth=auth)
    for message in response:
        context.bot.sendMessage(chat_id=update.message.chat_id, text=str(message))

def help(update, context):
    """send message"""
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Help!')

def reply(update, context):
    """send message"""
    message = update.message.text
    uname = update.message.chat.first_name if update.message.chat.first_name else ''+' '+ update.message.chat.last_name if update.message.chat.last_name else ''
    auth = {"telegram":update.message.chat_id}
    try:
        response = ChatBot(context.bot.token,channel=Channel.Telegram,uname=uname,auth=auth).reply(message)
        for message in response:
            context.bot.sendMessage(chat_id=update.message.chat_id, text=str(message))
    except Exception as e:
        print(e)
        context.bot.sendMessage(chat_id=update.message.chat_id, text='You are Restricted...!')
        context.bot.sendMessage(chat_id=update.message.chat_id, text='Sorry for the Inconvenience')