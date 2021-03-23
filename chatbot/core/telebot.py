
import importlib
from django.conf import settings
from django.apps import apps
import logging,os
import telegram
from telegram.ext import Dispatcher
from telegram.error import InvalidToken, TelegramError
from django_telegrambot.apps import DjangoTelegramBot,TELEGRAM_BOT_MODULE_NAME
from django.utils.module_loading import module_has_submodule

logger = logging.getLogger(__name__)

class TeleBot:
    @classmethod
    def module_exists(cls,module_name, method_name, execute):
        try:
            m = importlib.import_module(module_name)
            if execute and hasattr(m, method_name):
                logger.debug('Run {}.{}()'.format(module_name,method_name))
                getattr(m, method_name)()
            else:
                logger.debug('Run {}'.format(module_name))

        except ImportError as er:
            logger.debug('{} : {}'.format(module_name, repr(er)))
            return False
        return True

    @classmethod
    def setWebhook(cls,token):
        webhook_site = settings.DJANGO_TELEGRAMBOT.get('WEBHOOK_SITE', None)
        if not webhook_site:
            logger.warn('Required TELEGRAM_WEBHOOK_SITE missing in settings')
            return
        if webhook_site.endswith("/"):
            webhook_site = webhook_site[:-1]

        webhook_base = settings.DJANGO_TELEGRAMBOT.get('WEBHOOK_PREFIX','/')
        if webhook_base.startswith("/"):
            webhook_base = webhook_base[1:]
        if webhook_base.endswith("/"):
            webhook_base = webhook_base[:-1]

        cert = settings.DJANGO_TELEGRAMBOT.get('WEBHOOK_CERTIFICATE', None)
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
            DjangoTelegramBot.dispatchers.append(Dispatcher(bot, None, workers=0))
            hookurl = '{}/{}/{}/'.format(webhook_site, webhook_base, token)

            max_connections = 40

            setted = bot.setWebhook(hookurl, certificate=certificate, timeout=timeout, max_connections=max_connections, allowed_updates=allowed_updates,drop_pending_updates=True)
            webhook_info = bot.getWebhookInfo()
            real_allowed = webhook_info.allowed_updates if webhook_info.allowed_updates else ["ALL"]

            bot.more_info = webhook_info
            logger.info('Telegram Bot <{}> setting webhook [ {} ] max connections:{} allowed updates:{} pending updates:{} : {}'.format(bot.username, webhook_info.url, webhook_info.max_connections, real_allowed, webhook_info.pending_update_count, setted))
            print('Telegram Bot <{}> setting webhook [ {} ] max connections:{} allowed updates:{} pending updates:{} : {}'.format(bot.username, webhook_info.url, webhook_info.max_connections, real_allowed, webhook_info.pending_update_count, setted))
            
        except InvalidToken:
            logger.error('Invalid Token : {}'.format(token))
            return
        except TelegramError as er:
            logger.error('Error : {}'.format(repr(er)))
            logger.error('Error : {}'.format(repr(er)))
            return

        DjangoTelegramBot.bots.append(bot)
        DjangoTelegramBot.bot_tokens.append(token)
        DjangoTelegramBot.bot_usernames.append(bot.username)
        
        for app_config in apps.get_app_configs():
            if module_has_submodule(app_config.module, TELEGRAM_BOT_MODULE_NAME):
                module_name = '%s.%s' % (app_config.name, TELEGRAM_BOT_MODULE_NAME)
                if cls.module_exists(module_name, 'main', True):
                    logger.info('Loaded {}'.format(module_name))
    
    @classmethod
    def deleteWebhook(cls,token):
        try:
            bot = telegram.Bot(token=token)
            bot.delete_webhook(drop_pending_updates=True)
        except InvalidToken:
            logger.error('Invalid Token : {}'.format(token))
            return
        except TelegramError as er:
            logger.error('Error : {}'.format(repr(er)))
            return
        try:
            DjangoTelegramBot.bots.remove(bot)
            DjangoTelegramBot.bot_tokens.remove(token)
            DjangoTelegramBot.bot_usernames.remove(bot.username)
        except ValueError:
            pass
        
        for app_config in apps.get_app_configs():
            if module_has_submodule(app_config.module, TELEGRAM_BOT_MODULE_NAME):
                module_name = '%s.%s' % (app_config.name, TELEGRAM_BOT_MODULE_NAME)
                if cls.module_exists(module_name, 'main', True):
                    logger.info('Loaded {}'.format(module_name))
    
