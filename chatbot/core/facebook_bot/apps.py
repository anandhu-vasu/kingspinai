from django.apps import AppConfig
from django.conf import settings
import sqlalchemy as db
from chatbot.core.utils import Crypt

def _BOT_TOKENS()->list:
    try:
        engine = db.create_engine(settings.DATABASE_URL)
        connection = engine.connect()
        metadata = db.MetaData()
        chatbot = db.Table('core_chatbot', metadata, autoload=True, autoload_with=engine)   
        query = db.select([chatbot.columns.telegram_key]).where(chatbot.columns.telegram_status==1)
        result = connection.execute(query)
        rows = result.fetchall()
        if rows:
            return [ x[0] for x in rows]
        else:
            return []
    except:
        return []

def generate_facebook_verify_token(key:str,token:str)->str:
    return Crypt(key).hash()+Crypt(token).hash()

class FacebookBotConfig(AppConfig):
    name = 'chatbot.core.facebook_bot'
    label = 'facebook_bot'
    verbose_name = 'Facebook Bot'
    ready_run = False

    
