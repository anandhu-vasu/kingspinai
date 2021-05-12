from chatterbot.storage import StorageAdapter
from chatbot.core import chatbot, constants
from chatbot.core.exceptions import BotkeyNotFoundError
import json
import pickle
from pprint import pprint

class DjangoStorageAdapter(StorageAdapter):
    """
    Storage adapter that allows ChatterBot to interact with
    Django storage backends.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.django_app_name = kwargs.get(
            'django_app_name',
            constants.DEFAULT_DJANGO_APP_NAME
        )
        print(kwargs.get('botkey'))
        if 'botkey' in kwargs and kwargs.get('botkey'):
            Chatbot = self.get_model('chatbot')
            self.chatbot = Chatbot.objects.get(name=kwargs.get('botkey'))
        else:
            raise BotkeyNotFoundError()
        self.uname = kwargs.get('uname','')
    
    def get_chatbot_model(self):
        from django.apps import apps
        return apps.get_model(self.django_app_name, 'Chatbot')

    def get_statement_object(self):
        from chatbot.core.conversation import Statement
        return Statement

    @property
    def dataset(self):
        """ Returns the value of training dataset as python object """
        dataset = self.chatbot.training.dataset
        if not dataset:
            return []
        if isinstance(dataset,str):
            dataset = json.loads(dataset)
        return dataset

    @dataset.setter 
    def dataset(self, dataset):
        """ Accept & save python object to database """
        if isinstance(dataset,str):
            pprint(dataset)
            dataset = json.loads(dataset)
            pprint(dataset)
        self.chatbot.training.dataset = dataset
        self.chatbot.training.save()

    def gets_dataset(self)->str:
        """ Returns the value of training dataset as json string """
        dataset = self.chatbot.training.dataset
        if not dataset:
            return "[]"
        if not isinstance(dataset,str):
            dataset = json.dumps(dataset,separators=(',', ':'))
        return dataset

    def sets_dataset(self,dataset:str):
        """ Accept & try to save json string directly to database  """
        self.chatbot.training.dataset = dataset
        self.chatbot.training.save()

    @property
    def intent_model(self):
        """ Return the python object from bytes form """
        return pickle.loads(self.chatbot.training.intent_model)
    @intent_model.setter
    def intent_model(self,classifier):
        """ Save python object as bytes """
        self.chatbot.training.intent_model = pickle.dumps(classifier)
        self.chatbot.training.save()
    @property
    def ner_model(self):
        """ Return the python object from bytes form """
        return pickle.loads(self.chatbot.training.ner_model)
    @ner_model.setter
    def ner_model(self,ner):
        """ Save python object as bytes """
        self.chatbot.training.ner_model = pickle.dumps(ner)
        self.chatbot.training.save()
    @property
    def data_url(self):
        return self.chatbot.data_url
    @property
    def data_key(self):
        return self.chatbot.data_key
    @property
    def messages(self):
        """ Returns the value of training dataset as python object """
        messages = self.chatbot.messages
        if isinstance(messages,str):
            messages = json.loads(messages)
        return messages
    
