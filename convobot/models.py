from django.db import models
from django.conf import settings

import string
import random

from django.utils import timezone


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
