
from django.urls import re_path
from . import views
from django.conf import settings

webhook_base = "telegram_bot/"

urlpatterns = [
    re_path(r'admin/django-telegrambot/$', views.home, name='django-telegrambot'),
    re_path(r'{}(?P<bot_token>.+?)/$'.format(webhook_base), views.webhook, name='webhook.telegram'),
]
