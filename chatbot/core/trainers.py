from chatterbot import utils
from chatterbot.trainers import Trainer
from chatbot.core.conversation import Statement
from chatbot.core.corpus import Corpus
from chatbot.core.exceptions import EmptyTrainingDataError
from textblob.classifiers import NaiveBayesClassifier
import spacy
import random
from spacy.util import minibatch, compounding
import re

# from concurrent.futures import ThreadPoolExecutor

def trainNER(training_data):
    n_iter=100
    model = None
    nlp = spacy.blank("en")
    print("Created blank 'en' model")

    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)

    else:
        ner = nlp.get_pipe("ner")


    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        if model is None:
            nlp.begin_training()
        # optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(training_data)
            losses = {}

            batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,
                    annotations,
                    drop=0.5,
                    losses=losses,
                    # sgd=optimizer
                )
            print("Losses", losses)
    
    return nlp

def trainIntent(training_data):
    n_iter=30
    nlp = spacy.blank("en")
    model = None
    print("Created blank 'en' model")

    if "textcat" not in nlp.pipe_names:
        textcat=nlp.create_pipe( "textcat", config={"exclusive_classes": True, "architecture": "simple_cnn"})
        nlp.add_pipe(textcat, last=True)
    else:
        textcat = nlp.get_pipe("textcat")

    for _, annotations in training_data:
        for intent in annotations.get("cats").keys():
            if (intent not in textcat.labels):
                textcat.add_label(intent)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'textcat']
    with nlp.disable_pipes(*other_pipes):  # only train textcat
        # optimizer = nlp.begin_training()
        if model is None:
            nlp.begin_training()

        print("Training the model...")

        # Performing training
        for i in range(n_iter):
            random.shuffle(training_data)
            losses = {}
            batches = minibatch(training_data, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations,
                #  sgd=optimizer,
                 drop=0.2,losses=losses)
            print("Losses", losses)
        
        return nlp


class SophisticatedTrainer(Trainer):
    def train(self, *corpus_data):
        dataset = self.chatbot.storage.dataset
        corpus_data = list(corpus_data)
        if dataset:
            corpus_data.extend(dataset)
        if not corpus_data:
            raise EmptyTrainingDataError()

        intent_dataset = []
        ner_dataset = []
        repatt = r"\|([\w ,.']+)\|~([_A-Z]+)~"
        
        # 
        intents = []
        for story in corpus_data:
            for conversation in story["conversations"]:
                intent = conversation.get("intent")
                if intent:
                    intents.append(intent)
        # 

        for corpus,categories,name in Corpus.load_from_dic(*corpus_data):
            # statements_to_create = []

            for conversation_count, conversation in enumerate(corpus):
                if self.show_training_progress:
                    utils.print_progress_bar(
                        'Training ' + str(name),
                        conversation_count + 1,
                        len(corpus)
                    )
                
                for stm in conversation["statements"]:
                    if conversation["intent"]:
                        text = stm
                        ents = []
                        while True:
                            match = re.search(repatt,text);
                            if not match:
                                break
                            start_index = match.span()[0]
                            ents.append([start_index,start_index+len(match.group(1)),match.group(2)])
                            text = re.sub(repatt,r"\1",text,1)
                            
                        ner_dataset.append([text,{"entities":ents}])
                        
                        cats = {intent:(1 if conversation["intent"]==intent else 0) for intent in intents}
                        intent_dataset.append([text.lower(),{"cats":cats}])
                        
                        # intent_dataset.append([text.lower(),conversation["intent"]])

        # self.chatbot.storage.intent_model = NaiveBayesClassifier(intent_dataset)
        
        self.chatbot.storage.intent_model = trainIntent(intent_dataset)
        self.chatbot.storage.ner_model = trainNER(ner_dataset)
        
        # with ThreadPoolExecutor(max_workers=2) as executor:
        #     intent_future = executor.submit(trainIntent,intent_dataset)
        #     entity_future = executor.submit(trainNER,ner_dataset)
        #     self.chatbot.storage.intent_model = intent_future.result()
        #     self.chatbot.storage.ner_model = entity_future.result()


# x={
#     "name":""
#     "categories":[],
#     "conversations":[
#         {
#             "intent":""
#             "statements":[""],
#             "responses":[""]
#         }
#     ]
# }
