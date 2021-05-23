from chatbot.core.chatbot import Channel, ChatBot
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,ChatAction
import re

import logging
from pprint import pprint
logger = logging.getLogger(__name__)

reg_media = r"(<(image|video)\|(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))>)"


def message_controller(bot,chat_id,response):
    """ Identify and call specific send functions for different messsage types """
    skipiter: bool = False
    for i,message in enumerate(response):
        if skipiter:
            skipiter=False
            continue
        if message:
            if isinstance(message,dict):
                if message["type"] == 'buttons':
                    keyboard = [[InlineKeyboardButton(button['label'],callback_data=button['callback'])] for button in message["buttons"]]
                    bot.sendMessage(chat_id=chat_id,text="Try this :)",reply_markup=InlineKeyboardMarkup(keyboard))
            elif isinstance(message,str) and not message.isspace():
                reply_markup = {}
                if i+1 < len(response):# Check for next element
                    if isinstance(response[i+1],dict):# Next element is a dict
                        if response[i+1]["type"] == 'buttons':
                            keyboard = [[InlineKeyboardButton(button['label'],callback_data=button['callback'])] for button in response[i+1]["buttons"]]
                            reply_markup = {"reply_markup":InlineKeyboardMarkup(keyboard)}
                            skipiter = True#Skip next iteration ie exclude next dict element
                            
                match = re.search(reg_media,message)
                if match:
                    if(match.groups()[1]=='image'):
                        bot.send_chat_action(chat_id=chat_id,action=ChatAction.UPLOAD_PHOTO)
                        bot.send_photo(chat_id=chat_id,photo=match.groups()[2],**reply_markup)
                    elif match.groups()[1]=='video':
                        bot.send_chat_action(chat_id=chat_id,action=ChatAction.UPLOAD_VIDEO)
                        bot.send_video(chat_id=chat_id, video=match.groups()[2], supports_streaming=True,**reply_markup)
                else:
                    bot.sendMessage(chat_id=chat_id, text=str(message),**reply_markup)



def start_handler(update, context):
    """Send a message when the command /start is issued."""
    context.bot.send_chat_action(chat_id=update.message.chat_id,action=ChatAction.TYPING)
    def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
        return text.split()[1] if len(text.split()) > 1 else ''
    uid = extract_unique_code(update.message.text)
    auth = {"telegram":update.message.chat_id}
    uname = update.message.chat.first_name if update.message.chat.first_name else ''+' '+ update.message.chat.last_name if update.message.chat.last_name else ''
    response = ChatBot.intro(context.bot.token,channel=Channel.Telegram,uid=uid,uname=uname,auth=auth)
    message_controller(context.bot,update.message.chat_id,response)
            

def help(update, context):
    """send message"""
    context.bot.sendMessage(chat_id=update.message.chat_id, text='Help!')

def text_handler(update, context,message:str=None):
    """Handle received text messages"""
    context.bot.send_chat_action(chat_id=update.message.chat_id,action=ChatAction.TYPING)
    message = update.message.text if message==None else message
    uname = update.message.chat.first_name if update.message.chat.first_name else ''+' '+ update.message.chat.last_name if update.message.chat.last_name else ''
    auth = {"telegram":update.message.chat_id}
    try:
        response = ChatBot(context.bot.token,channel=Channel.Telegram,uname=uname,auth=auth).reply(message)
        
        message_controller(context.bot,update.message.chat_id,response)

    except Exception as e:
        print(e)
        context.bot.sendMessage(chat_id=update.message.chat_id, text='We are unable to process the response...!')
        context.bot.sendMessage(chat_id=update.message.chat_id, text='Sorry for the Inconvenience')
    
def voice_handler(update, context):
    """Handle received voice messages"""
    try:
        context.bot.send_chat_action(chat_id=update.message.chat_id,action=ChatAction.TYPING)
        
        bot = context.bot
        file = bot.getFile(update.message.voice.file_id)
        print(update)
        voice = 'temp/{}.ogg'.format(update.message.voice.file_id)
        file.download(voice)
        uname = update.message.chat.first_name if update.message.chat.first_name else ''+' '+ update.message.chat.last_name if update.message.chat.last_name else ''
        auth = {"telegram":update.message.chat_id}
        
        response = ChatBot(context.bot.token,channel=Channel.Telegram,uname=uname,auth=auth).replyFromVoice(voice)
        
        message_controller(context.bot,update.message.chat_id,response)

    except Exception as e:
        print(e)
        logger.error("Error: {}".format(e))
        context.bot.sendMessage(chat_id=update.message.chat_id, text='We are unable to process the response...!')
        context.bot.sendMessage(chat_id=update.message.chat_id, text='Sorry for the Inconvenience')
        
def button_handler(update, context):
    """
    Callback method handling button press
    """
    
    query: CallbackQuery = update.callback_query
    query.answer()

    text_handler(query,context,"{}".format(query.data))
    