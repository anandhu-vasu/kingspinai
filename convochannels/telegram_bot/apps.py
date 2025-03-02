import logging
import os

import telegram
from django.apps import AppConfig
from django.conf import settings
from telegram.error import InvalidToken, TelegramError
from telegram.ext import (CallbackQueryHandler, CommandHandler, Dispatcher,
                          Filters, MessageHandler)

from . import handlers

logger = logging.getLogger(__name__)

class TelegramBotConfig(AppConfig):
    name = 'convochannels.telegram_bot'
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
        if TelegramBotConfig.ready_run:return
        TelegramBotConfig.ready_run = True

        try:
            from convobot.models import Chatbot
            bot_tokens = Chatbot.objects.filter(telegram_status=True).values_list('telegram_key',flat=True)
            for bot_token in bot_tokens:
                TelegramBot.setWebhook(bot_token)
        except Exception as e:
            logger.error("Telegram Error on Ready: {}".format(e))


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
            
            dispatcher.add_handler(CommandHandler("start", handlers.start_handler))
            # dispatcher.add_handler(CommandHandler("help", help))
            dispatcher.add_handler(MessageHandler(Filters.text, handlers.text_handler))
            dispatcher.add_handler(MessageHandler(Filters.voice, handlers.voice_handler))
            dispatcher.add_handler(CallbackQueryHandler(handlers.button_handler))

    @classmethod
    def setWebhook(cls,token):

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
            hookurl = settings.WEBHOOK_URL.format(webhook_name='telegram_bot',bot_token=token)
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
        
