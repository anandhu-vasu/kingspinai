from django.conf import settings
import sqlalchemy as db

def _BOT_KEYS()->list:
    try:
        engine = db.create_engine(settings.DATABASE_URL)
        connection = engine.connect()
        metadata = db.MetaData()
        chatbot = db.Table('core_chatbot', metadata, autoload=True, autoload_with=engine)   
        query = db.select([chatbot.columns.telegram_key]).where(chatbot.columns.telegram_status==1)
        result = connection.execute(query)
        return [ {'TOKEN':x[0]} for x in result.fetchall()]
    except:
        return [{'TOKEN':'123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'}]


DJANGO_TELEGRAMBOT = {

    'MODE' : 'WEBHOOK', #(Optional [str]) # The default value is WEBHOOK,
                        # otherwise you may use 'POLLING'
                        # NB: if use polling you must provide to run
                        # a management command that starts a worker

    'WEBHOOK_SITE' : 'https://kingspin-ai.herokuapp.com',
    'WEBHOOK_PREFIX' : '/telegrambot', # (Optional[str]) # If this value is specified,
                                  # a prefix is added to webhook url                 #certificate.(More info at https://core.telegram.org/bots/self-signed )

    'BOTS' : _BOT_KEYS(),

}
# {
#    'TOKEN': '1591577456:AAFoSp4IrLO0u293iRqyIQW0iOcd9Ml3OW0', #Your bot token.
# },