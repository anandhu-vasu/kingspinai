from django.urls import path
from . import api_views as api

api_urlpatterns = [
    path('test/',api.UserAPIView.as_view(),name='test'),
    path('bot/chat/',api.ChatAPIView.as_view(),name='chat')
]
