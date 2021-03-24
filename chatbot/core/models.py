from chatterbot.ext.django_chatterbot.abstract_models import AbstractBaseStatement, AbstractBaseTag
from django.db import models
from django.conf import settings

import string,random

from django.utils import timezone
   
def id_generator(size=10, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

def default_messages():
    return dict(INTRO="Hi, ~uname~\nHow can I help you?",UNKNOWN="Sorry, I don't Understand")

class Chatbot(models.Model):
    """ 
    Chatbot model has training dataset for chatbot and trained ner models
    Name is a unique string accepted from user - used to identify bot
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="chatbots")
    name = models.SlugField(max_length=255,unique=True,null=True)
    telegram_status = models.BooleanField(default=False)
    telegram_key = models.CharField(max_length=255,null=True,unique=True)
    data_url = models.URLField(max_length=255,null=True)
    data_key = models.CharField(max_length=255,null=True)
    messages = models.JSONField(default=default_messages)
    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        if not self.name:
            self.name = id_generator()
            while Chatbot.objects.filter(name=self.name).exists():
                self.name = id_generator()
        super().save(*args, **kwargs)

class Training(models.Model):
    chatbot = models.OneToOneField(Chatbot,on_delete=models.CASCADE)
    dataset = models.JSONField(default=list)
    intent_model = models.BinaryField(null=True)
    ner_model = models.BinaryField(null=True)

# class Statement(AbstractBaseStatement):
#     """
#     A statement represents a single spoken entity, sentence or
#     phrase that someone can say.
#     """
#     chatbot = models.ForeignKey(Chatbot,on_delete=models.CASCADE,related_name="statements")


# class Tag(AbstractBaseTag):
#     """
#     A label that categorizes a statement.
#     """

