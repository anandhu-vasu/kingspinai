from django.urls import re_path
from . import views

webhook_base = "facebook_bot/"

urlpatterns = [
    re_path(r'{}(?P<bot_token>.+?)/$'.format(webhook_base), views.FacebookWebhook.as_view(  ), name='webhook.telegram'),

]