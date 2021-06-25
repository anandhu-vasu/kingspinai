from django.urls import re_path
from . import views
from django.conf import settings


urlpatterns = [
    re_path(settings.RE_WEBHOOK_URL.format(
        webhook_name='training_status'), views.TrainingStatusWebhook().as_view(), name=''),
    re_path(settings.RE_WEBHOOK_URL.format(
        webhook_name='register_lts_verification'), views.LTSRegistrationWebhook().as_view(), name=''),
]
