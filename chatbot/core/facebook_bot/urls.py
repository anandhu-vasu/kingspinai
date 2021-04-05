from django.conf.urls import url
from . import views

webhook_base = "facebook_bot/"

urlpatterns = [
    url(r'{}(?P<bot_token>.+?)/$'.format(webhook_base), views.FacebookWebhook.as_view(  ), name='webhook.telegram'),

]