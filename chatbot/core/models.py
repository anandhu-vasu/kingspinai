from chatterbot.ext.django_chatterbot.abstract_models import AbstractBaseStatement, AbstractBaseTag
from django.db import models
   

class Chatbot(models.Model):
    """ 
    Chatbot model has training dataset for chatbot and trained ner models
    Name is a unique string accepted from user - used to identify bot
    """
    name = models.CharField(max_length=255,unique=True,null=False)
    telegram_status = models.BooleanField(default=False)
    telegram_key = models.CharField(max_length=255,null=True)
    dataset = models.JSONField(default=list)
    ner_model = models.BinaryField(null=True)

    def __str__(self):
        return self.name


class Statement(AbstractBaseStatement):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """
    chatbot = models.ForeignKey(Chatbot,on_delete=models.CASCADE,related_name="statements")


class Tag(AbstractBaseTag):
    """
    A label that categorizes a statement.
    """

