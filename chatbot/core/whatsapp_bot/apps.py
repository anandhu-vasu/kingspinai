from django.apps import AppConfig


class WhatsappBotConfig(AppConfig):
    name = 'chatbot.core.whatsapp_bot'
    label = 'whatsapp_bot'
    verbose_name = 'Whatsapp Bot'
    ready_run = False  
    
