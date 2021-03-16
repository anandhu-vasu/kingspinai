import random
from chatterbot.logic import LogicAdapter
import re
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
        # cat = self.chatbot.storage.intent_model
        intent_classifier = self.chatbot.storage.intent_model
        print()
        print("TEXT: ",doc)
        try:
            prob = intent_classifier.prob_classify(doc.lower())
            intent = prob.max()
            confidence = prob.prob(intent)
            # confidence,intent = max((p, v) for (v, p) in cat(doc.lower()).cats.items())
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
