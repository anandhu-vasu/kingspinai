from chatterbot import utils
from chatterbot.trainers import Trainer
from django.db import models
from chatbot.core.conversation import Statement
from chatbot.core.corpus import Corpus
from chatbot.core.exceptions import EmptyTrainingDataError
from textblob.classifiers import NaiveBayesClassifier
import spacy
import random
from spacy.util import minibatch, compounding
import re

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
                )
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
        repatt = r"(\w+)\|~([_A-Z]+)~"

        for corpus,categories,name in Corpus.load_from_dic(*corpus_data):
            statements_to_create = []

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
                        intent_dataset.append([text,conversation["intent"]])
                    else:
                        for res in conversation["responses"]:
                            statement_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(stm)
                            response_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(res)

                            statement = Statement(
                                text=res,
                                search_text=response_search_text,
                                in_response_to=stm,
                                search_in_response_to=statement_search_text,
                                conversation='training'
                            )

                            statement.add_tags(*categories)

                            statement = self.get_preprocessed_statement(statement)

                            statements_to_create.append(statement)
            self.chatbot.storage.create_many(statements_to_create)

        self.chatbot.storage.intent_model = NaiveBayesClassifier(intent_dataset)
        self.chatbot.storage.ner_model = trainNER(ner_dataset)


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
