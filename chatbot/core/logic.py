import random
from chatterbot.logic import LogicAdapter
import re
from textblob import TextBlob
from chatterbot.conversation import Statement
from chatbot.core import exceptions

class Ingenious(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)


    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):
        
        dataset = self.chatbot.storage.dataset
        doc = str(statement)
        ent_pat = r"~([_A-Z]+)~"
        val_pat = r"~([_a-z]+)~"
        
        intent = None
        # Randomly select a confidence between 0 and 1
        IntentClassifier = self.chatbot.storage.intent_model
        

        # intent classification
        try:
            text_blob = TextBlob(doc, classifier=IntentClassifier)
            for sentence in text_blob.sentences:
                intent = sentence.classify()
        except:
            pass
        
        if intent:
            #Get all entities from all statements of the obtainted intent
            statement_entities:set = set()
            for story in dataset:
                for conversation in story["conversations"]:
                    if intent == conversation['intent']:
                        for smt in conversation["statements"]:
                            statement_entities.update(set(re.findall(r"\|~([_A-Z]+)~",smt)))

            #Entity Extraction
            extracted_entities = {}
            ner = self.chatbot.storage.ner_model
            doc = ner(doc)

            for ent in doc.ents:
                extracted_entities.setdefault(ent.label_,[]).append(ent.text)

            if statement_entities == set(extracted_entities.keys()):
                for story in dataset:
                    for conversation in story["conversations"]:
                        if intent == conversation['intent']:
                            res = random.choice(conversation["responses"])
                            if res:
                                while True:
                                    match = re.search(ent_pat,res);
                                    if not match:
                                        break
                                    try:
                                        res = re.sub(ent_pat,", ".join(extracted_entities[match.group(1)]),res,1)
                                    except:
                                        raise exceptions.NonExtractedEntityOnReply()
                                data = None
                                if data:
                                    for di,dv in enumerate(data):
                                        if di!=0:
                                            res+"\n"
                                        while True:
                                            match = re.search(val_pat,res);
                                            if not match:
                                                break
                                            try:
                                                res = re.sub(val_pat,dv[match.group(1)],res,1)
                                            except:
                                                raise exceptions.NonExtractedValueOnReply()
                                        


                                response = Statement(text=res)
                                response.confidence = 1
                                return response
    
        response = Statement(text="Sorry, I don't understand.")
        response.confidence = 0
        return response
