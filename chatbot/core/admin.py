from django.contrib import admin
from chatterbot.ext.django_chatterbot.model_admin import TagAdmin
from chatbot.core.models import Chatbot

@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('name','user','telegram_status','facebook_status','whatsapp_status','data_url','created_at')
    list_filter = ('user','telegram_status','facebook_status','whatsapp_status','created_at', )
    search_fields = ('name','user','telegram_key','facebook_status','whatsapp_status')
