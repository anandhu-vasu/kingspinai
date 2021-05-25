from django.urls import re_path
from . import views

webhook_base = "whatsapp_bot/"

urlpatterns = [
    re_path(r'{}(?P<bot_token>.+?)/$'.format(webhook_base), views.WhatsappWebhook.as_view(  ), name='webhook.whatsapp'),

]