from django.urls import re_path
from convobot.constants import RE_WEBHOOK_URL
from . import views

urlpatterns = [
    re_path(RE_WEBHOOK_URL.format(
        webhook_name='messenger_bot'), views.MessengerWebhook.as_view(), name='webhook.messenger'),

]
