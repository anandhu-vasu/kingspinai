from django.urls import path
from . import api_views as api

api_urlpatterns = [
    path('bot/chat/',api.ChatAPIView.as_view(),name='chat')
]
