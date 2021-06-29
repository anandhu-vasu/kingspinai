from . import handlers
import os

import telegram
from django.conf import settings
from telegram.error import InvalidToken, TelegramError
from telegram.ext import (CallbackQueryHandler, CommandHandler, Dispatcher,
                          Filters, MessageHandler)
import logging
logger = logging.getLogger(__name__)
from django.core.cache import caches
cache = caches['telegram_bot_dispatcher']

class TelegramBot:

    # @classmethod
    def getDispatcher(cls, token=None):
        return cache.get(f"{token}.dispatcher", None)

    @classmethod
    def getBot(cls, token=None):
        return cache.get(f"{token}.bot", None)

    @classmethod
    def addHandler(cls, token):
        dispatcher = cls.getDispatcher(token)  # get by bot token
        if dispatcher:

            dispatcher.add_handler(CommandHandler(
                "start", handlers.start_handler))
            # dispatcher.add_handler(CommandHandler("help", help))
            dispatcher.add_handler(MessageHandler(
                Filters.text, handlers.text_handler))
            dispatcher.add_handler(MessageHandler(
                Filters.voice, handlers.voice_handler))
            dispatcher.add_handler(
                CallbackQueryHandler(handlers.button_handler))

    @classmethod
    def setWebhook(cls, token):

        try:
            cert = settings.WEBHOOK_CERTIFICATE
        except:
            cert = None
        certificate = None
        if cert and os.path.exists(cert):
            logger.info('WEBHOOK_CERTIFICATE found in {}'.format(cert))
            certificate = open(cert, 'rb')
        elif cert:
            logger.error('WEBHOOK_CERTIFICATE not found in {} '.format(cert))

        allowed_updates = None
        timeout = None
        try:
            bot = telegram.Bot(token=token)
            dispatcher = Dispatcher(bot, None, workers=1)
            # cache.set(f"{token}.dispatcher",dispatcher )
            hookurl = settings.WEBHOOK_URL.format(
                webhook_name='telegram_bot', bot_token=token)
            max_connections = 40

            setted = bot.setWebhook(hookurl, certificate=certificate, timeout=timeout,
                                    max_connections=max_connections, allowed_updates=allowed_updates, drop_pending_updates=True)
            webhook_info = bot.getWebhookInfo()
            real_allowed = webhook_info.allowed_updates if webhook_info.allowed_updates else [
                "ALL"]

            bot.more_info = webhook_info
            logger.info('Telegram Bot <{}> setting webhook [ {} ] max connections:{} allowed updates:{} pending updates:{} : {}'.format(
                bot.username, webhook_info.url, webhook_info.max_connections, real_allowed, webhook_info.pending_update_count, setted))

        except InvalidToken:
            logger.error('Invalid Token : {}'.format(token))
            return
        except TelegramError as er:
            logger.error('Error : {}'.format(er))
            return

        cache.set(f"{token}.bot", bot)

        cls.addHandler(token)

    @classmethod
    def deleteWebhook(cls, token):
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
            cache.delete(f"{token}.bot")
            cache.delete(f"{token}.dispatcher")
        except ValueError:
            pass
