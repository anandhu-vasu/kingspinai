from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import *
from django.contrib import messages


@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'telegram_status',
                    'messenger_status', 'whatsapp_status', 'data_url', 'created_at')
    list_filter = ('user', 'telegram_status', 'messenger_status',
                   'whatsapp_status', 'created_at', )
    search_fields = ('name', 'user', 'telegram_key',
                     'messenger_status', 'whatsapp_status')
    
@admin.register(LTS)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('chatbot', 'url', 'token','botsign','dataset_ok')
    # list_filter = ('user', 'telegram_status', 'messenger_status',
    #                'whatsapp_status', 'created_at', )
    # search_fields = ('name', 'user', 'telegram_key',
    #                  'messenger_status', 'whatsapp_status')
    
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        try:
            obj.save()
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)
    

