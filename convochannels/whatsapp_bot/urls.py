from convobot.constants import RE_WEBHOOK_URL
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(RE_WEBHOOK_URL.format(
        webhook_name='whatsapp_bot'), views.WhatsappWebhook.as_view(), name='webhook.whatsapp'),

]
