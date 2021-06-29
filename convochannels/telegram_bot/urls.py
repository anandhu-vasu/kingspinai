
from django.urls import re_path
from . import views
from convobot.constants import RE_WEBHOOK_URL


urlpatterns = [
    re_path(r'admin/django-telegrambot/$', views.home, name='django-telegrambot'),
    re_path(RE_WEBHOOK_URL.format(
        webhook_name='telegram_bot'), views.webhook, name='webhook.telegram'),
]
