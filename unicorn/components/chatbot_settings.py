from chatbot.core.telebot import TeleBot
from django_unicorn.components import UnicornView
from django import forms
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
import telegram
from chatbot.core.models import Chatbot
from django_telegrambot.apps import DjangoTelegramBot,TELEGRAM_BOT_MODULE_NAME
from django.apps import apps

import logging

logger = logging.getLogger(__name__)



def validate_chatbot_telegram_key(token):
    try:
        telegram.Bot(token=token).username
    except:
        raise ValidationError(message="Invalid telegram bot api token.",code="invalid")
    else:
        return token


class ChatbotSettingsForm(forms.ModelForm):
    name = forms.SlugField(required=True,max_length=100,min_length=3)
    telegram_key = forms.CharField(max_length=255,required=False,validators=[validate_chatbot_telegram_key])

    class Meta:
        model = Chatbot
        fields = ('name', 'telegram_key', 'telegram_status','data_url','data_key')
        error_messages = {
            
        }

    def __init__(self,data, *args, **kwargs):
        cb = {}
        if isinstance(data['chatbot'],dict):
            cb = data['chatbot']
        elif isinstance(data['chatbot'],Chatbot):
            cb = model_to_dict(data['chatbot'],fields=[field.name for field in data['chatbot']._meta.fields])

        super().__init__(cb,*args, **kwargs)
    
    def validate_unique(self):
        """
        Call the instance's validate_unique() method and update the form's
        validation errors if any were raised.
        """
        exclude = self._get_validation_exclusions()
        try:
            self.instance.validate_unique(exclude=[*exclude,'name','telegram_key'])
        except ValidationError as e:
            self._update_errors(e)

        try:
            self.validate_unique_chatbot("name")
        except ValidationError as e:
            self._update_errors(e)
            
        try:
            self.validate_unique_chatbot("telegram_key")
        except ValidationError as e:
            self._update_errors(e)

    def validate_unique_chatbot(self,field):
        try:
            val = self.data[field]
            try:
                pk=self.data["pk"]
            except:
                pk=self.data["id"]
            if Chatbot.objects.exclude(pk=pk).filter(**{field:val}).exists():
                raise ValidationError({field:[ValidationError(message=f"Chatbot with this {field.replace('_',' ').title()} already exists.",code="unique")]})
            return val
        except KeyError:
            pass
        
class ChatbotSettingsView(UnicornView):
    form_class = ChatbotSettingsForm

    chatbot = None
    cached_name=None
    telegram_bot = None

    def updated(self, name, value):
        self.call("showErrors")

    def updated_chatbot_name(self, value):
        if self.is_valid(['name']):
            self.chatbot.save(update_fields=['name'])
            self.cached_name = self.chatbot.name
            self.call("refreshChatbotSettingsComponent")

    def updated_chatbot_data_url(self, value):
        if self.is_valid(['data_url']):
            self.chatbot.save(update_fields=['data_url'])

    def updated_chatbot_data_key(self, value):
        if self.is_valid(['data_key']):
            self.chatbot.save(update_fields=['data_key'])

    def updated_chatbot_telegram_key(self, value):
        if self.is_valid(['telegram_key']):
            self.chatbot.save(update_fields=["telegram_key"])
            if self.chatbot.telegram_key:
                try:
                    self.telegram_bot = telegram.Bot(token=self.chatbot.telegram_key).username
                except:
                    pass
            else:
                self.chatbot.telegram_status = False
                self.chatbot.save(update_fields=["telegram_status"])
                self.telegram_bot = False
        else:
            self.chatbot.telegram_status = False
            self.chatbot.save(update_fields=["telegram_status"])
            self.telegram_bot = False
            

    def updated_chatbot_telegram_status(self,value):
        if self.is_valid(['telegram_status']):
            self.chatbot.save(update_fields=['telegram_status'])
            if self.chatbot.telegram_status:
                TeleBot.setWebhook(self.chatbot.telegram_key)
            else:
                TeleBot.deleteWebhook(self.chatbot.telegram_key)
            

    def set_chatbot(self,pk):
        self.reset()
        self.errors.clear()
        self.chatbot = self.request.user.chatbots.get(pk=pk)
        # self.chatbot = list(self.request.user.chatbots.values("id","name","data_url","data_key","telegram_status","telegram_key").get(id=pk))
        self.cached_name=self.chatbot.name
        try:
            self.telegram_bot = telegram.Bot(token=self.chatbot.telegram_key).username
        except:
            self.telegram_bot = None
        self.call("openChatbotSettings")
