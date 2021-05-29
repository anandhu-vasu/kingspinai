from django.apps import AppConfig
from django.conf import settings
from chatbot.core.utils import Crypt

def generate_facebook_verify_token(key:str,token:str)->str:
    return Crypt(key).hash()+Crypt(token).hash()

class FacebookBotConfig(AppConfig):
    name = 'chatbot.core.facebook_bot'
    label = 'facebook_bot'
    verbose_name = 'Facebook Bot'
    ready_run = False

    
