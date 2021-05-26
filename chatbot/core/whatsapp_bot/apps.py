from django.apps import AppConfig
import logging
from django.conf import settings
import sqlalchemy as db
import requests
from chatbot.core.crypt import Encrypt

logger = logging.getLogger(__name__)

def _WHATSAPP_API_KEYS()->list:
    try:
        engine = db.create_engine(settings.DATABASE_URL)
        connection = engine.connect()
        metadata = db.MetaData()
        chatbot = db.Table('core_chatbot', metadata, autoload=True, autoload_with=engine)   
        query = db.select([chatbot.columns.whatsapp_key]).where(chatbot.columns.whatsapp_status==1)
        result = connection.execute(query)
        rows = result.fetchall()
        if rows:
            return [ x[0] for x in rows]
        else:
            return []
    except:
        return []

class WhatsappBotConfig(AppConfig):
    name = 'chatbot.core.whatsapp_bot'
    label = 'whatsapp_bot'
    verbose_name = 'Whatsapp Bot'
    ready_run = False
    
    def ready(self) -> None:
        
        if WhatsappBotConfig.ready_run:return
        WhatsappBotConfig.ready_run = True

        try:
            from chatbot.core.models import Chatbot
            api_keys = Chatbot.objects.filter(whatsapp_status=True).values_list('whatsapp_key',flat=True)
            for api_key in api_keys:
                set_whatsapp_webhook(api_key)
        except Exception as e:
            logger.error("Whatsapp Error on Ready: {}".format(e))
    
    
def set_whatsapp_webhook(api_key,delete=False):
    url = "https://waba.360dialog.io/v1/configs/webhook"
    payload ={
        "url": "https:" if delete else "{}/whatsapp_bot/{}/".format(settings.WEBHOOK_SITE[:-1] if settings.WEBHOOK_SITE.endswith("/") else settings.WEBHOOK_SITE,Encrypt(api_key).base64urlstrip.substitution()),
        "headers": {
            "Content-Type": "application/json",
        }
    }
    headers = {
        'D360-Api-Key': api_key,
        'Content-Type': "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)