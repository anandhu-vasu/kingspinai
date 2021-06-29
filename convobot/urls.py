from .constants import RE_WEBHOOK_URL
from django.urls import re_path

from . import views


urlpatterns = [
    re_path(RE_WEBHOOK_URL.format(
        webhook_name='training_status'), views.TrainingStatusWebhook.as_view(), name=''),
    re_path(RE_WEBHOOK_URL.format(
        webhook_name='register_lts_verification'), views.LTSRegistrationWebhook.as_view(), name=''),
]
