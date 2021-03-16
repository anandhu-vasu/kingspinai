from chatterbot.storage import StorageAdapter
from chatbot.core import chatbot, constants
from chatbot.core.exceptions import BotkeyNotFoundError
import json
import pickle

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
            self.chatbot = Chatbot.objects.defer("dataset","ner_model","intent_model").get(name=kwargs.get('botkey'))
        else:
            raise BotkeyNotFoundError()

    def get_statement_model(self):
        from django.apps import apps
        return apps.get_model(self.django_app_name, 'Statement')

    def get_tag_model(self):
        from django.apps import apps
        return apps.get_model(self.django_app_name, 'Tag')
    
    def get_chatbot_model(self):
        from django.apps import apps
        return apps.get_model(self.django_app_name, 'Chatbot')

    def count(self):
        Statement = self.get_model('statement')
        return Statement.objects.count()

    def get_statement_object(self):
        from chatbot.core.conversation import Statement

        StatementModel = self.get_model('statement')
        Statement.statement_field_names.extend(
            StatementModel.extra_statement_field_names
        )
        return Statement

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        from django.db.models import Q

        kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        persona_not_startswith = kwargs.pop('persona_not_startswith', None)
        search_text_contains = kwargs.pop('search_text_contains', None)

        # Convert a single sting into a list if only one tag is provided
        if type(tags) == str:
            tags = [tags]

        if tags:
            kwargs['tags__name__in'] = tags

        statements = self.chatbot.statements.filter(**kwargs)

        if exclude_text:
            statements = statements.exclude(
                text__in=exclude_text
            )

        if exclude_text_words:
            or_query = [
                ~Q(text__icontains=word) for word in exclude_text_words
            ]

            statements = statements.filter(
                *or_query
            )

        if persona_not_startswith:
            statements = statements.exclude(
                persona__startswith='bot:'
            )

        if search_text_contains:
            or_query = Q()

            for word in search_text_contains.split(' '):
                or_query |= Q(search_text__contains=word)

            statements = statements.filter(
                or_query
            )

        if order_by:
            statements = statements.order_by(*order_by)

        for statement in statements.iterator():
            yield statement

    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        tags = kwargs.pop('tags', [])
        if not kwargs["chatbot"]:
            kwargs["chatbot"]=self.chatbot

        if 'search_text' not in kwargs:
            kwargs['search_text'] = self.tagger.get_bigram_pair_string(kwargs['text'])

        if 'search_in_response_to' not in kwargs:
            if kwargs.get('in_response_to'):
                kwargs['search_in_response_to'] = self.tagger.get_bigram_pair_string(kwargs['in_response_to'])

        statement = Statement(**kwargs)

        statement.save()

        tags_to_add = []

        for _tag in tags:
            tag, _ = Tag.objects.get_or_create(name=_tag)
            tags_to_add.append(tag)

        statement.tags.add(*tags_to_add)

        return statement

    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        tag_cache = {}

        for statement in statements:

            statement_data = statement.serialize()
            tag_data = statement_data.pop('tags', [])
            if not statement_data["chatbot"]:
                statement_data["chatbot"] = self.chatbot


            statement_model_object = Statement(**statement_data)

            if not statement.search_text:
                statement_model_object.search_text = self.tagger.get_bigram_pair_string(statement.text)

            if not statement.search_in_response_to and statement.in_response_to:
                statement_model_object.search_in_response_to = self.tagger.get_bigram_pair_string(statement.in_response_to)

            statement_model_object.save()

            tags_to_add = []

            for tag_name in tag_data:
                if tag_name in tag_cache:
                    tag = tag_cache[tag_name]
                else:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    tag_cache[tag_name] = tag
                tags_to_add.append(tag)

            statement_model_object.tags.add(*tags_to_add)

    def update(self, statement):
        """
        Update the provided statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        if hasattr(statement, 'id'):
            statement.save()
        else:
            statement = Statement.objects.create(
                text=statement.text,
                search_text=self.tagger.get_bigram_pair_string(statement.text),
                conversation=statement.conversation,
                in_response_to=statement.in_response_to,
                search_in_response_to=self.tagger.get_bigram_pair_string(statement.in_response_to),
                created_at=statement.created_at,
                chatbot=self.chatbot,
            )

        for _tag in statement.tags.all():
            tag, _ = Tag.objects.get_or_create(name=_tag)

            statement.tags.add(tag)

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """

        statement = self.chatbot.statements.order_by('?').first()

        if statement is None:
            raise self.EmptyDatabaseException()

        return statement

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """

        statements = self.chatbot.statements.filter(text=statement_text)

        statements.delete()

    def drop(self):
        """
        Remove all data from the database.
        """
        Tag = self.get_model('tag')
        tag_ids=self.chatbot.statements.values_list("tags",flat=True)
        tag_ids=list(set(tag_ids)) 
        self.chatbot.statements.all().delete()
        Tag.objects.filter(id__in=tag_ids).delete()

    @property
    def dataset(self):
        """ Returns the value of training dataset as python object """
        dataset = self.chatbot.dataset
        if not dataset:
            return []
        if isinstance(dataset,str):
            dataset = json.loads(dataset)
        return dataset

    @dataset.setter 
    def dataset(self, dataset):
        """ Accept & save python object to database """
        if isinstance(dataset,str):
            dataset = json.loads(dataset)
        self.chatbot.dataset = dataset
        self.chatbot.save()

    def gets_dataset(self)->str:
        """ Returns the value of training dataset as json string """
        dataset = self.chatbot.dataset
        if not dataset:
            return "[]"
        if not isinstance(dataset,str):
            dataset = json.dumps(dataset,separators=(',', ':'))
        return dataset

    def sets_dataset(self,dataset:str):
        """ Accept & try to save json string directly to database  """
        self.chatbot.dataset = dataset
        self.chatbot.save()

    @property
    def intent_model(self):
        """ Return the python object from bytes form """
        return pickle.loads(self.chatbot.intent_model)
    @intent_model.setter
    def intent_model(self,classifier):
        """ Save python object as bytes """
        self.chatbot.intent_model = pickle.dumps(classifier)
        self.chatbot.save()
    @property
    def ner_model(self):
        """ Return the python object from bytes form """
        return pickle.loads(self.chatbot.ner_model)
    @ner_model.setter
    def ner_model(self,ner):
        """ Save python object as bytes """
        self.chatbot.ner_model = pickle.dumps(ner)
        self.chatbot.save()
    
    
