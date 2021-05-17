from telegram import bot
from chatbot.core.facebook_bot.apps import generate_facebook_verify_token
from chatbot.core.models import Chatbot
from chatbot.core.chatbot import Channel, ChatBot
from chatbot.core.utils import Decrypt
from django.views.decorators.csrf import csrf_exempt

from django.views import generic
from django.http.response import HttpResponse
import json,requests
import re

reg_media = r"(<(image|video)\|(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))>)"


def post_facebook_message(access_token,fbid,message):
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
    attachment_data = json.dumps({"message":{"attachment":{"type":media_type, "payload":{"url":url,}}}})
    attachment = requests.post(attachment_url, headers={"Content-Type": "application/json","Accept": "application/json"}, data=attachment_data,).json()
    print(attachment)
    
    return attachment['attachment_id']

def post_facebook_media(access_token,fbid,media_type,attachment_id):
    post_message_url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(access_token)
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"attachment":{"type":media_type, "payload":{"attachment_id": attachment_id}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

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
    start_button_load = json.dumps({ "get_started":{"payload":"GET_STARTED"}})
    status = requests.post(start_button_url, headers={"Content-Type": "application/json"},data=start_button_load)

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
            status = Chatbot.objects.only('facebook_status','facebook_key').get(facebook_key = bot_token ).facebook_status
        except:
            status = False
        if status:
            # Converts the text payload into a python dictionary
            incoming_message = json.loads(self.request.body.decode('utf-8'))
            print(incoming_message)
            # Facebook recommends going through every entry since they might send
            # multiple messages in a single call during high load
            for entry in incoming_message['entry']:
                for message in entry['messaging']:
                    # Check to make sure the received call is a message call
                    # This might be delivery, optin, postback for other events 
                    try:
                        if 'message' in message:
                        # Print the message to the terminal
                            msg = message['message']['text']
                            user = get_facebook_user(bot_token,message['sender']['id'])
                            uname = user['first_name'] if user['first_name'] else ''
                            auth = {"facebook":message['sender']['id']}
                        
                            response = ChatBot(bot_token,channel=Channel.Facebook,uname=uname,auth=auth).reply(msg)
                            for msg in response:
                                if msg:
                                    match = re.search(reg_media,msg)
                                    if match:
                                        media_type=match.groups()[1]
                                        post_facebook_media(bot_token,message['sender']['id'],media_type,upload_attachment(bot_token,media_type,url=match.groups()[2]))
                                    else:
                                        post_facebook_message(bot_token,message['sender']['id'], str(msg))
                            
                        elif 'postback' in message:
                            if message['postback']['title'] == "Get Started":
                                uid = ''
                                if 'referral' in message['postback']:
                                    uid = message['postback']['referral']['ref']
                                user = get_facebook_user(bot_token,message['sender']['id'])
                                uname = user['first_name'] if user['first_name'] else ''
                                auth = {"facebook":message['sender']['id']}
                                response = ChatBot.intro(bot_token,channel=Channel.Facebook,uid=uid,uname=uname,auth=auth)
                                for msg in response:
                                    if msg:
                                        match = re.search(reg_media,msg)
                                        if match:
                                            media_type=match.groups()[1]
                                            post_facebook_media(bot_token,message['sender']['id'],media_type,upload_attachment(bot_token,media_type,url=match.groups()[2]))
                                        else:
                                            post_facebook_message(bot_token,message['sender']['id'], str(msg))
                                
                    except Exception as e:
                        print(e)
                        post_facebook_message(bot_token,message['sender']['id'], "Sorry for the Inconvenience.")
                        post_facebook_message(bot_token,message['sender']['id'], "We can't process the response") 
            
        return HttpResponse()
