from chatbot.core.utils import Encrypt
from chatbot.core.telegram_bot import TelegramBot
from django_unicorn.components import UnicornView,UnicornField
from django import forms
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
import telegram,re
from chatbot.core.models import Chatbot
from django.conf import settings
from chatbot.core.facebook_bot.apps import generate_facebook_verify_token
from chatbot.core.facebook_bot.views import get_facebook_page
from chatbot.core.whatsapp_bot.views import get_whatsapp_id
from chatbot.core.whatsapp_bot.apps import set_whatsapp_webhook
import logging

logger = logging.getLogger(__name__)

class ChatbotMessages(UnicornField):
    
    def __init__(self, *args, **kwargs):
        self.INTRO = kwargs.get("INTRO","")
        self.UNKNOWN = kwargs.get("UNKNOWN","")
    

def validate_chatbot_telegram_key(token):
    try:
        telegram.Bot(token=token).username
    except:
        raise ValidationError(message="Invalid telegram bot api token.",code="invalid")
    else:
        return token

def validate_chatbot_facebook_key(token):
    if get_facebook_page(token) == None:
        raise ValidationError(message="Invalid facebook page access token.",code="invalid")
    else:
        return token
    
def validate_chatbot_whatsapp_key(token):
    if get_whatsapp_id(token) == None:
        raise ValidationError(message="Invalid facebook page access token.",code="invalid")
    else:
        return token

class ChatbotSettingsForm(forms.ModelForm):
    name = forms.SlugField(required=True,max_length=100,min_length=3)
    telegram_key = forms.CharField(max_length=255,required=False,validators=[validate_chatbot_telegram_key])
    facebook_key = forms.CharField(max_length=255,required=False,validators=[validate_chatbot_facebook_key])
    whatsapp_key = forms.CharField(max_length=255,required=False,validators=[validate_chatbot_whatsapp_key])

    class Meta:
        model = Chatbot
        fields = ('name', 'telegram_key', 'telegram_status','facebook_key', 'facebook_status','whatsapp_key', 'whatsapp_status','data_url','data_key')
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
            self.instance.validate_unique(exclude=[*exclude,'name','telegram_key','facebook_key','whatsapp_key'])
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
        try:
            self.validate_unique_chatbot("facebook_key")
        except ValidationError as e:
            self._update_errors(e)
        try:
            self.validate_unique_chatbot("whatsapp_key")
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
    messages = None
    cached_name=None
    telegram_bot = None
    whatsapp_bot = None
    facebook_bot = None
    facebook_verify_token = ""
    facebook_url = ""
    tab = "general"

    def updated(self, name, value):
        if name.startswith("messages."):
            value = re.sub(r" +", " ", value)
            value = re.sub(r"\n+", "\n", value)
            if isinstance(self.messages,ChatbotMessages):
                setattr(self.messages,name.split('.',1)[1],value.strip())
                self.chatbot.messages = self.messages.to_json()
                self.chatbot.save(update_fields=['messages'])
        self.call("showErrors")

    def updated_chatbot_name(self, value):
        if self.is_valid(['name']):
            self.chatbot.save(update_fields=['name'])
            self.cached_name = self.chatbot.name
            self.set_facebook_verify_token()
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
                TelegramBot.setWebhook(self.chatbot.telegram_key)
            else:
                TelegramBot.deleteWebhook(self.chatbot.telegram_key)
            
    def updated_chatbot_facebook_key(self, value):

        if self.is_valid(['facebook_key']):
            self.chatbot.save(update_fields=["facebook_key"])
            if self.chatbot.facebook_key:
                self.facebook_bot = get_facebook_page(self.chatbot.facebook_key)
            else:
                self.chatbot.facebook_status = False
                self.chatbot.save(update_fields=["facebook_status"])
                self.facebook_bot = False
            self.set_facebook_verify_token()
            self.set_facebook_url()
        else:
            self.chatbot.facebook_status = False
            self.chatbot.save(update_fields=["facebook_status"])
            self.facebook_bot = False
            
    def updated_chatbot_facebook_status(self,value):
        if self.is_valid(['facebook_status']):
            self.chatbot.save(update_fields=['facebook_status'])
            
    def set_facebook_verify_token(self):
        if self.chatbot.facebook_key:
                self.facebook_verify_token = generate_facebook_verify_token(self.cached_name,self.chatbot.facebook_key)
        else: self.facebook_verify_token = ""
    
    def set_facebook_url(self):
        if self.chatbot.facebook_key:
            self.facebook_url = "{}/facebook_bot/{}/".format(settings.WEBHOOK_SITE[:-1] if settings.WEBHOOK_SITE.endswith("/") else settings.WEBHOOK_SITE,Encrypt(self.chatbot.facebook_key).base64urlstrip.substitution())
        else:
            self.facebook_url = ""
            
    def updated_chatbot_whatsapp_key(self, value):
        if self.is_valid(['whatsapp_key']):
            self.chatbot.save(update_fields=["whatsapp_key"])
            if self.chatbot.whatsapp_key:
                self.whatsapp_bot = get_whatsapp_id(self.chatbot.whatsapp_key,format=True)
            else:
                self.chatbot.whatsapp_status = False
                self.chatbot.save(update_fields=["whatsapp_status"])
                self.whatsapp_bot = False
        else:
            self.chatbot.whatsapp_status = False
            self.chatbot.save(update_fields=["whatsapp_status"])
            self.whatsapp_bot = False
            
    def updated_chatbot_whatsapp_status(self,value):
        if self.is_valid(['whatsapp_status']):
            self.chatbot.save(update_fields=['whatsapp_status'])
            if self.chatbot.whatsapp_status:
                set_whatsapp_webhook(self.chatbot.whatsapp_key)
            else:
                set_whatsapp_webhook(self.chatbot.whatsapp_key,delete=True)

    def set_chatbot(self,pk):
        self.errors.clear()
        if self.request:
            self.chatbot = self.request.user.chatbots.get(pk=pk)
            self.messages = ChatbotMessages(**self.chatbot.messages)
            # self.chatbot = list(self.request.user.chatbots.values("id","name","data_url","data_key","telegram_status","telegram_key").get(id=pk))
            self.cached_name=self.chatbot.name
            self.set_facebook_verify_token()
            self.set_facebook_url()
            self.tab = "general"
            try:
                self.telegram_bot = telegram.Bot(token=self.chatbot.telegram_key).username if self.chatbot.telegram_key else None
            except:
                self.telegram_bot = None
            self.facebook_bot = get_facebook_page(self.chatbot.facebook_key) if self.chatbot.facebook_key else None
            self.whatsapp_bot = get_whatsapp_id(self.chatbot.whatsapp_key,format=True) if self.chatbot.whatsapp_key else None
            self.call("openChatbotSettings")
        else:
            self.call("resetChatbotSettings")

    def set_tab(self,tab):
        self.tab = tab
        self.call("tabLoaded")
