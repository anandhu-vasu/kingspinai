from django.contrib import admin
from chatterbot.ext.django_chatterbot.model_admin import TagAdmin
from chatbot.core.models import Statement, Tag, Chatbot

@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'in_response_to', 'conversation', 'created_at','chatbot' )
    list_filter = ('text', 'created_at', )
    search_fields = ('text', )

@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('name','user','telegram_key','telegram_status','dataset','created_at')
    list_filter = ('name','user','telegram_status','created_at', )
    search_fields = ('name','user','telegram_key')

admin.site.register(Tag, TagAdmin)