from convobot.reply_message import ReplyButtonList, ReplyMedia, ReplyText
from convobot.models import Chatbot
from convobot.convobot import Convobot
from convochannels import ConvoChannels
from crypt.crypt import Decrypt
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.http.response import HttpResponse
import json,requests
import re
from django.core.cache import caches
cache = caches['last_message_id']


api_url = "https://waba.360dialog.io/v1"

def get_whatsapp_id(api_key,format=False):
    try:
        wa_id_url = "{}/configs/phone_number".format(api_url)
        headers={"D360-API-KEY":api_key,"Content-Type": "application/json","Accept": "application/json"}
        res = requests.get(wa_id_url, headers=headers).json()
        if 'phone_number' in res:
            return "+{} {}".format(res['phone_number'][:2],res['phone_number'][2:]) if format and len(res['phone_number']) > 10 else res['phone_number']
    except:
        pass
    return None


    
def post_whatsapp_text_message(api_key,wa_id,text):
    text_url = f"{api_url}/messages"
    payload = {
            "to": wa_id,
            "type": "text",
            "text": {
                "body": text
            }
        }
    headers = {
        'D360-Api-Key': api_key,
        'Content-Type': "application/json",
    }
    requests.post(text_url, json=payload, headers=headers)

def post_whatsapp_media(api_key,wa_id,media_type,url):
    media_url = f"{api_url}/messages"
    payload = {
        "to": wa_id,
        "type": media_type,
        media_type: {
            "link": url,
        }
    }
    headers = {
        'D360-Api-Key': api_key,
        'Content-Type': "application/json",
    }
    requests.post(media_url, json=payload, headers=headers)

def get_whatsapp_voice(api_key,voice_id):
    headers = {
        'D360-Api-Key': api_key,
        'Content-Type': "application/json",
    }
    try:
        voice = requests.get("https://waba.360dialog.io/v1/media/"+voice_id, headers=headers).content
        voice_path = 'temp/{}.opus'.format(voice_id)
        
        with open(voice_path, "wb") as file:
            file.write(voice)
            return voice_path
    except:
        return None

def put_message_status_read(api_key,msg_id:str):
    message_status_url = "https://waba.360dialog.io/v1/messages/"+msg_id
    headers = {
        'D360-Api-Key': api_key,
        'Content-Type': "application/json",
    }
    payload = {"status": "read"}
    requests.put(message_status_url,json=payload,headers=headers)

def message_controller(api_key,wa_id,response):
    """ Identify and send specific reply for each message type """
    skipiter: bool = False
    for i,message in enumerate(response):
        if skipiter:
            skipiter=False
            continue
        if message:
            if isinstance(message,ReplyButtonList):
                    buttons = [{"type":"postback","title":(button.label[:18] + '..') if len(button.label) > 20 else button.label,"payload":button.callback} for button in message if button.label.isspace()]
                    # post_postback_button(api_key,wa_id,":)",buttons)
            elif isinstance(message,ReplyText) and not message.text.isspace():
                post_whatsapp_text_message(api_key, wa_id, str(message.text))
            elif isinstance(message,ReplyMedia):
                post_whatsapp_media(api_key,wa_id,message.type,url=message.url)

class WhatsappWebhook(generic.View):
    # def get(self,request, bot_token):
    #     try: 
    #         key=Chatbot.objects.get(whatsapp_key=bot_token).name
    #         if self.request.GET['hub.verify_token'] == generate_whatsapp_verify_token(key,bot_token):
    #             set_start_button(bot_token)
    #             return HttpResponse(self.request.GET['hub.challenge'])
    #     except:
    #         pass
    #     return HttpResponse('Error, invalid token')
        
    @csrf_exempt
    def dispatch(self,*args,**kwargs):
        if 'bot_token' in kwargs:
            kwargs['bot_token'] = Decrypt(kwargs['bot_token']).substitution.base64urlstrip()
        return generic.View.dispatch(self,*args,**kwargs)    # Post function to handle Whatsapp messages

    def post(self,request, bot_token):
        
        try:
            chatbot = Chatbot.objects.only('name', 'whatsapp_status', 'whatsapp_key').get(whatsapp_key=bot_token)
            status  = chatbot.whatsapp_status
        except:
            status = False
        if status:
            
            # Converts the text payload into a python dictionary
            incoming_message = json.loads(self.request.body.decode('utf-8'))
            # print(incoming_message)
            # whatsapp recommends going through every entry since they might send
            # multiple messages in a single call during high load
            try:
                if 'contacts' in incoming_message and 'messages' in incoming_message:
                    uname = incoming_message['contacts'][0]['profile']['name']
                    wa_id = incoming_message['contacts'][0]['wa_id']
                    message_type = incoming_message["messages"][0]["type"]
                    message_id = incoming_message["messages"][0]["id"]
                    auth = {"whatsapp":wa_id}
                    
                    if cache.get(f"chatbots.{chatbot.name}.{ConvoChannels.WHATSAPP}.{wa_id}.last_message_id") == message_id:
                        return HttpResponse()
                    else:
                        cache.set(
                            f"chatbots.{chatbot.name}.{ConvoChannels.WHATSAPP}.{wa_id}.last_message_id", message_id)
                    
                    if message_type == 'text':
                        put_message_status_read(bot_token,message_id)
                        text = incoming_message["messages"][0]["text"]["body"]
                        response = Convobot(bot_token,channel=ConvoChannels.WHATSAPP,uname=uname,auth=auth).reply_messages(text)
                        message_controller(bot_token,wa_id,response)
                    elif message_type == 'voice':
                        put_message_status_read(bot_token,message_id)
                        voice_id =  incoming_message["messages"][0]["voice"]["id"]
                        voice = get_whatsapp_voice(bot_token,voice_id)
                        response = Convobot(bot_token,channel=ConvoChannels.WHATSAPP,uname=uname,auth=auth).replyFromVoice(voice)
                        message_controller(bot_token,wa_id,response)
                        
            except Exception as e:
                print(e)
                post_whatsapp_text_message(bot_token,wa_id, "Sorry for the Inconvenience.")
                post_whatsapp_text_message(bot_token,wa_id, "We can't process the response")
            # finally:
            #     post_sender_action(bot_token,message['sender']['id'],"typing_off")
            
        return HttpResponse()
