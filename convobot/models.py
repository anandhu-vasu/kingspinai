from convobot.schemas import Authorization
from convobot.exceptions import LTSTokenError
from django.db import models
from django.conf import settings

import string
import random
import uuid
import requests

from django.utils import timezone
from crypt.crypt import Encrypt


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def default_messages():
    return dict(INTRO="Hi, ~uname~\nHow can I help you?", UNKNOWN="Sorry, I don't Understand")


class Chatbot(models.Model):
    """ 
    Chatbot model has training dataset for chatbot and trained ner models
    Name is a unique string accepted from user - used to identify bot
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="chatbots")
    name = models.SlugField(max_length=255, unique=True, null=True)
    telegram_status = models.BooleanField(default=False)
    telegram_key = models.CharField(max_length=255, null=True, unique=True)
    messenger_status = models.BooleanField(default=False)
    messenger_key = models.CharField(max_length=255, null=True, unique=True)
    whatsapp_status = models.BooleanField(default=False)
    whatsapp_key = models.CharField(max_length=255, null=True, unique=True)
    data_url = models.URLField(max_length=255, null=True)
    data_key = models.CharField(max_length=255, null=True)
    messages = models.JSONField(default=default_messages)
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = id_generator()
            while Chatbot.objects.filter(name=self.name).exists():
                self.name = id_generator()
        super().save(*args, **kwargs)

# class Training(models.Model):
#     chatbot = models.OneToOneField(Chatbot, on_delete=models.CASCADE)
#     dataset = models.JSONField(default=list)
#     intent_model = models.BinaryField(null=True)
#     ner_model = models.BinaryField(null=True)

class Auth(models.Model):
    chatbot = models.ForeignKey(
        Chatbot, on_delete=models.CASCADE, related_name="auth")
    uid = models.CharField(max_length=255)
    uname = models.CharField(max_length=255, null=True)
    telegram = models.PositiveIntegerField(null=True)
    messenger = models.PositiveIntegerField(null=True)
    whatsapp = models.PositiveIntegerField(null=True)

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

class Analytics(models.Model):
    chatbot = models.ForeignKey(
        Chatbot, on_delete=models.CASCADE, related_name="analytics")
    duration = models.PositiveSmallIntegerField()
    channel = models.CharField(max_length=100)
    confidence = models.DecimalField(null=True, max_digits=4, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)

class LTS(models.Model):
    chatbot = models.OneToOneField(
        Chatbot, on_delete=models.CASCADE, related_name="LTS",primary_key=True)
    botsign = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255,null=True,blank=True)#passsword
    url = models.URLField(null=True)
    training_status = models.PositiveSmallIntegerField(null=True,blank=True)
    dataset = models.JSONField(default=list,blank=True)
    dataset_ok = models.BooleanField(default=False,blank=True,editable=False)
    validation_token = models.CharField(
        null=True, max_length=255, blank=True, editable=False)
    
    __original_token = None
    __original_url = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_token = self.token
        self.__original_url = self.url
    
    def save(self, *args, **kwargs):
        if self.url :
            if self.url.endswith('/'):
                self.url =str(self.url)[:-1]
            if not self.token:
                self.token = ''.join(random.choices(
                    string.ascii_letters + string.digits + string.punctuation, k=16))
            if self.token and self.botsign:
                if self.__original_token == None:

                    valid_token = ''.join(random.choices(
                        string.ascii_uppercase + string.digits, k=24))
                    LTS.objects.filter(pk=self.pk).update(validation_token=valid_token)
                    callback_url = settings.WEBHOOK_URL.format(
                        webhook_name='register_lts_verification',
                        bot_token=Encrypt(
                            self.botsign).base64urlstrip.substitution.prependrandom()
                    )
                    payload={
                        "token": self.token,
                        "botsign": str(self.botsign),
                        "validation_token": valid_token,
                        "callback_url": callback_url
                    }
                    
                    res = requests.post(f"{self.url}/register", json=payload, headers={"Content-Type": "application/json", "Accept": "application/json", })
                    if not res.status_code == 200:
                        print(res.content)
                        raise LTSTokenError("LTS Registration Failed!")
                        
                elif self.__original_token != self.token or self.__original_url != self.url:
                    data = Authorization(token=self.token).json()
                    res = requests.post(f"{self.LTS.url}/token",
                                        data=data, headers=self._headers)
                    if not res.status_code == 200:
                        raise LTSTokenError("Failed to change LTS details!")

        
        super().save(*args, **kwargs)
