from django.apps import AppConfig
import logging
from django.conf import settings
import sqlalchemy as db

import os
import telegram
from telegram.ext import Dispatcher
from telegram.error import InvalidToken, TelegramError
from telegram.ext import CommandHandler, MessageHandler, Filters
from .handlers import *

logger = logging.getLogger(__name__)

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


class TelegramBotConfig(AppConfig):
    name = 'chatbot.core.telegram_bot'
    label = 'telegram_bot'
    verbose_name = 'Telegram Bot'
    ready_run = False
    bot_tokens = []
    bot_usernames = []
    dispatchers = []
    bots = []
    updaters = []
    __used_tokens = set()

    @classmethod
    def get_dispatcher(cls, bot_id=None, safe=True):
        if bot_id is None:
            cls.__used_tokens.add(cls.bot_tokens[0])
            return cls.dispatchers[0]
        else:
            try:
                index = cls.bot_tokens.index(bot_id)
            except ValueError:
                if not safe:
                    return None
                try:
                    index = cls.bot_usernames.index(bot_id)
                except ValueError:
                    return None
            cls.__used_tokens.add(cls.bot_tokens[index])
            return cls.dispatchers[index]
    
    @classmethod
    def get_bot(cls, bot_id=None, safe=True):
        if bot_id is None:
            if safe:
                return cls.bots[0]
            else:
                return None
        else:
            try:
                index = cls.bot_tokens.index(bot_id)
            except ValueError:
                if not safe:
                    return None
                try:
                    index = cls.bot_usernames.index(bot_id)
                except ValueError:
                    return None
            return cls.bots[index]

    @classmethod
    def get_updater(cls, bot_id=None, safe=True):
        if bot_id is None:
            return cls.updaters[0]
        else:
            try:
                index = cls.bot_tokens.index(bot_id)
            except ValueError:
                if not safe:
                    return None
                try:
                    index = cls.bot_usernames.index(bot_id)
                except ValueError:
                    return None
            return cls.updaters[index]

    def ready(self) -> None:
        if TelegramBotConfig.ready_run:
            return
        TelegramBotConfig.ready_run = True

        bot_tokens = _BOT_TOKENS()
        for bot_token in bot_tokens:
            TelegramBot.setWebhook(bot_token)


class TelegramBot:

    @classmethod
    def getDispatcher(cls, bot_id=None, safe=True):
        return TelegramBotConfig.get_dispatcher(bot_id, safe)

    @classmethod
    def getBot(cls, bot_id=None, safe=True):
        return TelegramBotConfig.get_bot(bot_id, safe)

    @classmethod
    def getUpdater(cls, id=None, safe=True):
        return TelegramBotConfig.get_updater(id, safe)

    @classmethod
    def addHandler(cls,token):
        dispatcher = cls.getDispatcher(token)     #get by bot token
        if dispatcher:
            dispatcher.add_handler(CommandHandler("start", start))
            # dispatcher.add_handler(CommandHandler("help", help))
            dispatcher.add_handler(MessageHandler(Filters.text, reply))
            dispatcher.add_handler(MessageHandler(Filters.voice, voice_handler))

    @classmethod
    def setWebhook(cls,token):
        try:
            webhook_site = settings.WEBHOOK_SITE
        except:
            logger.warn('Required TELEGRAM_WEBHOOK_SITE missing in settings')
            return
        if webhook_site.endswith("/"):
            webhook_site = webhook_site[:-1]

        webhook_base = "telegram_bot"
        if webhook_base.startswith("/"):
            webhook_base = webhook_base[1:]
        if webhook_base.endswith("/"):
            webhook_base = webhook_base[:-1]

        try:
            cert = settings.WEBHOOK_CERTIFICATE
        except:
            cert = None
        certificate = None
        if cert and os.path.exists(cert):
            logger.info('WEBHOOK_CERTIFICATE found in {}'.format(cert))
            certificate=open(cert, 'rb')
        elif cert:
            logger.error('WEBHOOK_CERTIFICATE not found in {} '.format(cert))

        allowed_updates = None
        timeout = None
        try:
            bot = telegram.Bot(token=token)
            TelegramBotConfig.dispatchers.append(Dispatcher(bot, None, workers=1))
            hookurl = '{}/{}/{}/'.format(webhook_site, webhook_base, token)

            max_connections = 40

            setted = bot.setWebhook(hookurl, certificate=certificate, timeout=timeout, max_connections=max_connections, allowed_updates=allowed_updates,drop_pending_updates=True)
            webhook_info = bot.getWebhookInfo()
            real_allowed = webhook_info.allowed_updates if webhook_info.allowed_updates else ["ALL"]

            bot.more_info = webhook_info
            logger.info('Telegram Bot <{}> setting webhook [ {} ] max connections:{} allowed updates:{} pending updates:{} : {}'.format(bot.username, webhook_info.url, webhook_info.max_connections, real_allowed, webhook_info.pending_update_count, setted))
            
        except InvalidToken:
            logger.error('Invalid Token : {}'.format(token))
            return
        except TelegramError as er:
            logger.error('Error : {}'.format(er))
            return

        TelegramBotConfig.bots.append(bot)
        TelegramBotConfig.bot_tokens.append(token)
        TelegramBotConfig.bot_usernames.append(bot.username)

        cls.addHandler(token)
    
    @classmethod
    def deleteWebhook(cls,token):
        try:
            bot = telegram.Bot(token=token)
            bot.delete_webhook(drop_pending_updates=True)
        except InvalidToken:
            logger.error('Invalid Token : {}'.format(token))
            return
        except TelegramError as er:
            logger.error('Error : {}'.format(er))
            return
        try:
            TelegramBotConfig.bots.remove(bot)
            TelegramBotConfig.bot_tokens.remove(token)
            TelegramBotConfig.bot_usernames.remove(bot.username)
            index = None
            try:
                index = TelegramBotConfig.bot_tokens.index(token)
            except ValueError:
                try:
                    index = TelegramBotConfig.bot_usernames.index(bot.username)
                except ValueError:
                    pass
            if index:
                del TelegramBotConfig.dispatchers[index]
        except ValueError:
            pass
        