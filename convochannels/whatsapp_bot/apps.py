from convochannels.telegram_bot.views import webhook
import logging

import requests
from crypt.crypt import Encrypt
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)

class WhatsappBotConfig(AppConfig):
    name = 'convochannels.whatsapp_bot'
    label = 'whatsapp_bot'
    verbose_name = 'Whatsapp Bot'
    ready_run = False
    
    def ready(self) -> None:
        
        if WhatsappBotConfig.ready_run:return
        WhatsappBotConfig.ready_run = True

        try:
            from convobot.models import Chatbot
            api_keys = Chatbot.objects.filter(whatsapp_status=True).values_list('whatsapp_key',flat=True)
            for api_key in api_keys:
                set_whatsapp_webhook(api_key)
        except Exception as e:
            logger.error("Whatsapp Error on Ready: {}".format(e))
    
    
def set_whatsapp_webhook(api_key,delete=False):
    url = "https://waba.360dialog.io/v1/configs/webhook"
    webhook_url = settings.WEBHOOK_URL.format(
        webhook_name='whatsapp_bot', bot_token=Encrypt(api_key).base64urlstrip.substitution())
    payload ={
        "url": "https:" if delete else webhook_url,
        "headers": {
            "Content-Type": "application/json",
        }
    }
    headers = {
        'D360-Api-Key': api_key,
        'Content-Type': "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
