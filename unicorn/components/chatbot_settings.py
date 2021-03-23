from chatbot.core.telegram_bot import TelegramBot
from django_unicorn.components import UnicornView,UnicornField
from django import forms
from django.core.exceptions import ValidationError
import telegram
from chatbot.core.models import Chatbot as ChatbotModel

import logging

logger = logging.getLogger(__name__)

class Chatbot(UnicornField):
    def __init__(self,chatbots,pk):
        fields = dict(chatbots.values("user","name","data_url","data_key","telegram_status","telegram_key","pk").get(pk=pk))
        self.pk = fields.get("pk")
        self.user = fields.get("user")
        self.name = fields.get("name")
        self.telegram_status = fields.get("telegram_status")
        self.telegram_key = fields.get("telegram_key")
        self.data_url = fields.get("data_url")
        self.data_key = fields.get("data_key")

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
        model = ChatbotModel
        fields = ('name', 'telegram_key', 'telegram_status','data_url','data_key')
        error_messages = {
            
        }

    def __init__(self,data, *args, **kwargs):
        
        cb = {}
        if isinstance(data['chatbot'],dict):
            cb = data['chatbot']
        elif isinstance(data['chatbot'],Chatbot):
            cb = data['chatbot'].to_json()#model_to_dict(data['chatbot'],fields=[field.name for field in data['chatbot']._meta.fields])
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
            if val:
                try:
                    pk=self.data["pk"]
                except:
                    pk=self.data["id"]
                if ChatbotModel.objects.exclude(pk=pk).filter(**{field:val}).exists():
                    print(field)
                    raise ValidationError({field:[ValidationError(message=f"Chatbot with this {field.replace('_',' ').title()} already exists.",code="unique")]})
            return val
        except KeyError:
            pass
        
class ChatbotSettingsView(UnicornView):
    form_class = ChatbotSettingsForm

    chatbot = None
    _chatbot = None
    cached_name = None
    telegram_bot = None

    def updated(self, name, value):
        self.call("showErrors")

    def updated_chatbot_name(self, value):
        self._chatbot.name = value
        if self.is_valid(['name']):
            self._chatbot.save(update_fields=['name'])
            self.cached_name = self._chatbot.name
            self.call("refreshChatbotSettingsComponent")

    def updated_chatbot_data_url(self, value):
        self._chatbot.data_url = value
        if self.is_valid(['data_url']):
            self._chatbot.save(update_fields=['data_url'])

    def updated_chatbot_data_key(self, value):
        self._chatbot.data_key = value
        if self.is_valid(['data_key']):
            self._chatbot.save(update_fields=['data_key'])

    def updated_chatbot_telegram_key(self, value):  
        self._chatbot.telegram_key = value if value else None
        if self.is_valid(['telegram_key']):
            self._chatbot.save(update_fields=["telegram_key"])
            if self.chatbot.telegram_key:
                try:
                    self.telegram_bot = telegram.Bot(token=self.chatbot.telegram_key).username
                except:
                    pass
            else:
                self.chatbot.telegram_status = False
                self._chatbot.save(update_fields=["telegram_status"])
                self.telegram_bot = False
        else:
            self.chatbot.telegram_status = False
            self._chatbot.save(update_fields=["telegram_status"])
            self.telegram_bot = False
            

    def updated_chatbot_telegram_status(self,value):
        self._chatbot.telegram_status = value
        if self.is_valid(['telegram_status']):
            self._chatbot.save(update_fields=['telegram_status'])
            if self.chatbot.telegram_status:
                TelegramBot.setWebhook(self.chatbot.telegram_key)
            else:
                TelegramBot.deleteWebhook(self.chatbot.telegram_key)
            

    def set_chatbot(self,pk):
        self.reset()
        self.errors.clear()
        if self.request:
            self._chatbot = self.request.user.chatbots.defer("dataset","ner_model","intent_model").get(pk=pk)
            self.chatbot = Chatbot(self.request.user.chatbots,pk)
            self.cached_name=self.chatbot.name
            try:
                self.telegram_bot = telegram.Bot(token=self.chatbot.telegram_key).username
            except:
                self.telegram_bot = None
            self.call("openChatbotSettings")


