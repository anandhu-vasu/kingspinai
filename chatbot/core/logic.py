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
        # prob_dict = IntentClassifier.prob_classify(doc.lower())._prob_dict
        # prob_dict.update((x, 2**y) for x, y in prob_dict.items())
        # print(prob_dict)
        # intent classification
        print()
        print("TEXT: ",doc)
        try:
            text_blob = TextBlob(doc.lower(), classifier=IntentClassifier)
            for sentence in text_blob.sentences:
                intent = sentence.classify()
                confidence = sentence.classifier.prob_classify(sentence.raw).prob(intent)
                print("INTENT: ",intent,confidence,(confidence >= 0.8))
                if confidence < 0.8:
                    response = Statement(text="Sorry, I don't understand.")
                    response.confidence = 0
                    return response
        except:
            pass
        
        if intent:
            #Get all entities from all statements of the obtainted intent
            statement_entities = set()
            for story in dataset:
                for conversation in story["conversations"]:
                    if intent == conversation['intent']:
                        for smt in conversation["statements"]:
                            statement_entities.update(set(re.findall(r"\w+\|~([_A-Z]+)~",smt)))

            #Entity Extraction
            extracted_entities = {}
            ner = self.chatbot.storage.ner_model
            doc = ner(doc)

            for ent in doc.ents:
                extracted_entities.setdefault(ent.label_,[]).append(ent.text)
            
            print("ENTITIES STATEMENT: ",statement_entities)
            print("ENTITIES EXTRACTED: ",extracted_entities)
            print()

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
