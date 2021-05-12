from chatbot.core.chatbot import Channel, ChatBot
import re

reg_media = r"(<(image|video)\|(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))>)"


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
        if message:
            match = re.search(reg_media,message)
            if match:
                if(match.groups()[1]=='image'):
                    context.bot.send_photo(chat_id=update.message.chat_id,photo=match.groups()[2])
                elif match.groups()[1]=='video':
                    context.bot.send_video(chat_id=update.message.chat_id, video=match.groups()[2], supports_streaming=True)
            else:
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
        
        print(response)
        for message in response:
            if message:
                match = re.search(reg_media,message)
                if match:
                    if(match.groups()[1]=='image'):
                        context.bot.send_photo(chat_id=update.message.chat_id,photo=match.groups()[2])
                    elif match.groups()[1]=='video':
                        context.bot.send_video(chat_id=update.message.chat_id, video=match.groups()[2], supports_streaming=True)
                else:
                    context.bot.sendMessage(chat_id=update.message.chat_id, text=str(message))
    except Exception as e:
        print(e)
        context.bot.sendMessage(chat_id=update.message.chat_id, text='You are Restricted...!')
        context.bot.sendMessage(chat_id=update.message.chat_id, text='Sorry for the Inconvenience')
    