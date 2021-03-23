
from django.conf.urls import url
from . import views
from django.conf import settings

webhook_base = "telegram_bot/"

urlpatterns = [
    url(r'admin/django-telegrambot/$', views.home, name='django-telegrambot'),
    url(r'{}(?P<bot_token>.+?)/$'.format(webhook_base), views.webhook, name='webhook'),
]
