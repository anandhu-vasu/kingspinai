from django.urls import path
from . import views

urlpatterns = [
    path('bot/chat/', views.WebchatAPIView.as_view(), name='webchat')
]
