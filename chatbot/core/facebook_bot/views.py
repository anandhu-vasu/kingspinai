from chatbot.core.facebook_bot.apps import generate_facebook_verify_token
from chatbot.core.models import Chatbot
from chatbot.core.chatbot import Channel, ChatBot
from chatbot.core.utils import Decrypt
from django.views.decorators.csrf import csrf_exempt

from django.views import generic
from django.http.response import HttpResponse
import json,requests
import re
from heap import Heap

reg_media = r"(<(image|video)\|(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))>)"


def post_facebook_text_message(access_token,fbid,message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(access_token)
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    # print(status.json())

def get_facebook_user(access_token,fbid,fields='first_name,last_name'):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':fields, 'access_token':access_token}
    user_details = requests.get(user_details_url, user_details_params).json()
    return user_details

def upload_attachment(access_token,media_type,url) -> str:
    attachment_url = "https://graph.facebook.com/v10.0/me/message_attachments?access_token={}".format(access_token)
    attachment_data = json.dumps({"message":{"attachment":{"type":media_type, "payload":{"url":url,"is_reusable":False}}}})
    attachment = requests.post(attachment_url, headers={"Content-Type": "application/json","Accept": "application/json"}, data=attachment_data,).json()
    print(attachment)
    
    return attachment['attachment_id']

def post_facebook_media(access_token,fbid,media_type,url):
    post_message_url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(access_token)
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":media_type, "payload":{"url": url}}}})
    # response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":media_type, "payload":{"attachment_id": attachment_id}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    
def post_postback_button(access_token,fbid,text,buttons):
    button_url = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(access_token)
    response_msg = {
        "recipient":{
            "id":fbid
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":text,
                    "buttons":buttons
                    # [
                    #     {
                    #         "type":"postback",
                    #         "title":label,
                    #         "payload": callback
                    #     }
                    # ]
                }
            }
        }
    }
    status = requests.post(button_url, headers={"Content-Type": "application/json"},json=response_msg)
    
def post_sender_action(access_token,fbid,action):
    """ To display a sender action in the conversation such as mark_seen,typing_on,typing_off """
    sender_action_url = "https://graph.facebook.com/v2.6/me/messages?access_token={}".format(access_token)
    response_msg = {"recipient":{"id":fbid}, "sender_action":action}
    status = requests.post(sender_action_url, headers={"Content-Type": "application/json"},json=response_msg)

def get_facebook_page(access_token):
    try:
        page_url = "https://graph.facebook.com/v2.6/me"
        page_access_token = {'access_token':access_token}
        page_details = requests.get(page_url, page_access_token).json()
        if 'id' in page_details and 'name' in page_details:
            return page_details
    except:
        pass
    return None

def set_start_button(access_token):
    start_button_url = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token={}".format(access_token)
    start_button_load = json.dumps({ "get_started":{"payload":"|@#GET_STARTED#@|"}})
    status = requests.post(start_button_url, headers={"Content-Type": "application/json"},data=start_button_load)


def message_controller(bot_token,fbid,response):
    """ Identify and send specific request for each message type """
    skipiter: bool = False
    for i,message in enumerate(response):
        if skipiter:
            skipiter=False
            continue
        if message:
            if isinstance(message,dict):
                if message["type"] == 'buttons':
                    buttons = [{"type":"postback","title":(button['label'][:18] + '..') if len(button['label']) > 20 else button['label'],"payload":button['callback']} for button in message["buttons"]]
                    post_postback_button(bot_token,fbid,":)",buttons)
            elif isinstance(message,str) and not message.isspace():
                   
                match = re.search(reg_media,message)
                if match:
                    media_type=match.groups()[1]
                    post_facebook_media(bot_token,fbid,media_type,url=match.groups()[2] )#upload_attachment(bot_token,media_type,url=match.groups()[2]))
                else:
                    post_facebook_text_message(bot_token,fbid, str(message))
    
class FacebookWebhook(generic.View):
    def get(self,request, bot_token):
        try: 
            key=Chatbot.objects.get(facebook_key=bot_token).name
            if self.request.GET['hub.verify_token'] == generate_facebook_verify_token(key,bot_token):
                set_start_button(bot_token)
                return HttpResponse(self.request.GET['hub.challenge'])
        except:
            pass
        return HttpResponse('Error, invalid token')
        
    @csrf_exempt
    def dispatch(self,*args,**kwargs):
        if 'bot_token' in kwargs:
            kwargs['bot_token'] = Decrypt(kwargs['bot_token']).substitution.base64urlstrip()
        return generic.View.dispatch(self,*args,**kwargs)    # Post function to handle Facebook messages

    def post(self,request, bot_token):
        try:
            chatbot = Chatbot.objects.only('name', 'facebook_status', 'facebook_key').get(facebook_key=bot_token)
            status  = chatbot.facebook_status
        except:
            status = False
        if status:
            # Converts the text payload into a python dictionary
            incoming_message = json.loads(self.request.body.decode('utf-8'))
            # print(incoming_message)
            # Facebook recommends going through every entry since they might send
            # multiple messages in a single call during high load 1621889927385
            
            for entry in incoming_message['entry']:
                for message in entry['messaging']:
                    # Check to make sure the received call is a message call
                    # This might be delivery, optin, postback for other events 
                    try:
                        fbid = message['sender']['id']
                        if 'message' in message:
                        # Print the message to the terminal
                            message_id = message['message']['mid']
                            
                            if Heap.get("chatbots",chatbot.name,Channel.Facebook,fbid,"last_message_id") == message_id:
                                return HttpResponse()
                            else:
                                Heap.set("chatbots",chatbot.name,Channel.Facebook,fbid,"last_message_id",val=message_id)
                            
                            post_sender_action(bot_token,fbid,"mark_seen")
                            post_sender_action(bot_token,fbid,"typing_on")
                            msg = message['message']['text']
                            user = get_facebook_user(bot_token,fbid)
                            uname = user['first_name'] if user['first_name'] else ''
                            auth = {"facebook":fbid}
                        
                            response = ChatBot(bot_token,channel=Channel.Facebook,uname=uname,auth=auth).reply(msg)
                            message_controller(bot_token,fbid,response)
                            
                        elif 'postback' in message:
                            timestamp = message['timestamp']
                            if Heap.get("chatbots",chatbot.name,Channel.Facebook,fbid,"last_timestamp") == timestamp:
                                return HttpResponse()
                            else:
                                Heap.set("chatbots",chatbot.name,Channel.Facebook,fbid,"last_timestamp",val=timestamp)
                            
                            if message['postback']['title'] == "Get Started" and message['postback']['payload']== '|@#GET_STARTED#@|':
                                post_sender_action(bot_token,fbid,"mark_seen")
                                post_sender_action(bot_token,fbid,"typing_on")
                                
                                uid = ''
                                if 'referral' in message['postback']:
                                    uid = message['postback']['referral']['ref']
                                user = get_facebook_user(bot_token,fbid)
                                uname = user['first_name'] if user['first_name'] else ''
                                auth = {"facebook":fbid}
                                response = ChatBot.intro(bot_token,channel=Channel.Facebook,uid=uid,uname=uname,auth=auth)
                                message_controller(bot_token,fbid,response)
                            elif message['postback']['payload']:# For postback buttons
                                post_sender_action(bot_token,fbid,"mark_seen")
                                post_sender_action(bot_token,fbid,"typing_on")
                                
                                msg = message['postback']['payload']
                                user = get_facebook_user(bot_token,fbid)
                                uname = user['first_name'] if user['first_name'] else ''
                                auth = {"facebook":fbid}
                            
                                response = ChatBot(bot_token,channel=Channel.Facebook,uname=uname,auth=auth).reply(msg)
                                message_controller(bot_token,fbid,response)
                                
                                
                                
                    except Exception as e:
                        print(e)
                        post_facebook_text_message(bot_token,fbid, "Sorry for the Inconvenience.")
                        post_facebook_text_message(bot_token,fbid, "We can't process the response")
                    finally:
                        post_sender_action(bot_token,fbid,"typing_off")
                        
            
        return HttpResponse()
