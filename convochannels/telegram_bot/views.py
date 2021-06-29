# coding=utf-8
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .apps import TelegramBot
from django.views.decorators.csrf import csrf_exempt
import sys
import json
import telegram
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@staff_member_required
def home(request):
    bot_list = TelegramBot.bots
    context = {'bot_list': bot_list, 'update_mode':'WEBHOOK'}
    return render(request, 'telegram_bot/index.html', context)


@csrf_exempt
def webhook (request, bot_token):

    #verifico la validità del token
    bot = TelegramBot.getBot(bot_token)
    if bot is None:
        logger.warn('Request for not found token : {}'.format(bot_token))
        return JsonResponse({})

    try:
        data = json.loads(request.body.decode("utf-8"))

    except:
        logger.warn('Telegram bot <{}> receive invalid request : {}'.format(bot.username, repr(request)))
        return JsonResponse({})

    dispatcher = TelegramBot.getDispatcher(bot_token)
    if dispatcher is None:
        logger.error('Dispatcher for bot <{}> not found : {}'.format(bot.username, bot_token))
        return JsonResponse({})

    try:
        update = telegram.Update.de_json(data, bot)
        dispatcher.process_update(update)
        logger.debug('Bot <{}> : Processed update {}'.format(bot.username, update))
    # Dispatch any errors
    except TelegramError as te:
        logger.warn("Bot <{}> : Error was raised while processing Update.".format(bot.username))
        dispatcher.dispatchError(update, te)

    # All other errors should not stop the thread, ju
    except:
        logger.error("Bot <{}> : An uncaught error was raised while processing an update\n{}".format(bot.username, sys.exc_info()[0]))

    finally:
        return JsonResponse({})
