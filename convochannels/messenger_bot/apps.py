from django.apps import AppConfig
from crypt.crypt import Crypt


def generate_facebook_verify_token(key: str, token: str) -> str:
    return Crypt(key).hash()+Crypt(token).hash()

class MessengerBotConfig(AppConfig):
    name = 'convochannels.messenger_bot'
    label = 'messenger_bot'
    verbose_name = 'messenger Bot'
    ready_run = False

    
