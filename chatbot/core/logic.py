import random
from chatterbot.logic import LogicAdapter
import re,requests
from django.contrib import auth
from chatterbot.conversation import Statement
from chatbot.core import exceptions
from pprint import pprint
import json

class Ingenious(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.uid = kwargs.get('uid','')
        self.uname = kwargs.get('uname','')
        self.is_auth = kwargs.get('is_auth',False)


    def can_process(self, statement):
        return True

    def process(self, statement, additional_response_selection_parameters=None):
        
        dataset = self.chatbot.storage.dataset
        doc = str(statement)
        ent_pat = r"~([_A-Z]+)~"
        val_pat = r"~([_a-z]+)~"
        
        intent = None
        cat = self.chatbot.storage.intent_model
        # intent_classifier = self.chatbot.storage.intent_model
        print()
        print("TEXT: ",doc)
        try:
            # prob = intent_classifier.prob_classify(doc.lower())
            # intent = prob.max()
            # confidence = prob.prob(intent)
            confidence,intent = max((p, v) for (v, p) in cat(doc.lower()).cats.items())
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
                            statement_entities.update(set(re.findall(r"\|[\w ,.']+\|~([_A-Z]+)~",smt)))

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
                            if conversation['auth'] and not self.is_auth:
                                raise exceptions.UnAuthenticated()
                            res = random.choice(conversation["responses"])
                            # for button in conversation['buttons']:
                                # res+="\n<buttons|{}|{}|>".format(button['label'],button['callback'])
                            if conversation['buttons']:
                                res+="\n<buttons|{}|>".format(json.dumps(conversation['buttons']))
                            
                            if res:
                                data = []
                                data_url = self.chatbot.storage.data_url
                                
                                res = re.sub(r"~uname~",self.chatbot.storage.uname,res)

                                if data_url:
                                    if conversation['data_fetch']:
                                        _data = {
                                            "api_key" : self.chatbot.storage.data_key,
                                            "uid" : self.uid,
                                            "intent" : intent,
                                            "entities" : extracted_entities
                                        }
                                        _headers = {'Content-Type': 'application/json','Accept':'application/json'}
                                        try:
                                            data_res = requests.post(data_url,data=json.dumps(_data),headers=_headers)
                                            print(data_res.json())
                                            if data_res.status_code == 200:
                                                data = data_res.json()
                                            elif data_res.status_code == 400:
                                                response = Statement(text="Sorry, I don't understand.")
                                                response.confidence = 0
                                                return response
                                        except:
                                            pass
                                if data:
                                    res_strp = res
                                    res = ""
                                    ei=0
                                    for di,dval in enumerate(data):
                                        if isinstance(dval,dict):
                                            res_str = res_strp
                                            increment_ei = False
                                            while True:
                                                match = re.search(ent_pat,res_str);
                                                if not match:
                                                    break
                                                try:
                                                    # if len(data) == 1:
                                                    #     res_str = re.sub(ent_pat,", ".join(extracted_entities[match.group(1)]),res_str,1)
                                                    # el
                                                    if len(extracted_entities[match.group(1)])==1:
                                                        res_str = re.sub(ent_pat,str(extracted_entities[match.group(1)][0]),res_str,1)
                                                    else:
                                                        res_str = re.sub(ent_pat,str(extracted_entities[match.group(1)][ei]),res_str,1)
                                                        increment_ei=True
                                                except:
                                                    raise exceptions.NonExtractedEntityOnReply()
                                            if increment_ei:
                                                ei+=1

                                            while True:
                                                match = re.search(val_pat,res_str);
                                                if not match:
                                                    break
                                                try:
                                                    res_str = re.sub(val_pat,str(dval[match.group(1)]),res_str,1)
                                                except Exception as e:
                                                    print(e)
                                                    raise exceptions.NonExtractedValueOnReply()
                                            if di!=0:
                                                res_str = "\n" +res_str
                                            res+=res_str
                                        elif isinstance(dval,str):
                                            if di!=0:
                                                dval = "\n" +dval
                                            res+=dval
                                else:
                                    match = re.search(ent_pat,res);
                                    if match != None:
                                        raise exceptions.NonExtractedValueOnReply()
                                    while True:
                                        match = re.search(ent_pat,res);
                                        if not match:
                                            break
                                        try:
                                            res = re.sub(ent_pat,", ".join(extracted_entities[match.group(1)]),res,1)
                                        except:
                                            raise exceptions.NonExtractedEntityOnReply()
                                        
                                response = Statement(text=res)
                                response.confidence = confidence
                                return response
    
        response = Statement(text="Sorry, I don't understand.")
        response.confidence = 0
        return response
