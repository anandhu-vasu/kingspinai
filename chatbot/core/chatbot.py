from chatbot.core.utils import Decrypt
from chatbot.core import exceptions
import chatbot
from chatterbot import ChatBot as Bot
from chatbot.core.config import CHATBOT_OPTIONS
from chatbot.core.trainers import SophisticatedTrainer
import re
from enum import Enum

class Channel(str,Enum):
    Web = "Web"
    Telegram = "Telegram"
    Facebook = "Facebook"


class ChatBot:
    def __init__(self,key,channel:Channel=Channel.Web,uid:str='',uname='',auth=None):
        from chatbot.core.models import Chatbot as ChatbotModel
        is_auth = False
        self.uid=uid
        if channel in Channel and channel != Channel.Web:
            chatbot = ChatbotModel.objects.get(**{"{}_key".format(channel.value.lower()):key})
        else:
            chatbot = ChatbotModel.objects.get(name = key)
        self.name = chatbot.name
        if uid:
            try:
                _auth = chatbot.auth.get(uid=uid)
                is_auth = True
                uname = _auth.uname if _auth.uname else uname

                if channel!=Channel.Web:
                    if auth:
                        _auth.update(**auth,uname=uname)
            except: pass
        elif auth and channel!=Channel.Web:
            try:
                _auth = chatbot.auth.get(**auth)
                is_auth = True
                uname = _auth.uname if _auth.uname else uname
            except: pass

        self.uname = uname
        self.chatbot = Bot(
            name = self.name,
            botkey = self.name,
            uname= self.uname,
            uid = self.uid,
            is_auth = is_auth,
            **CHATBOT_OPTIONS
        )

    def train(self):
        trainer = SophisticatedTrainer(self.chatbot)
        trainer.train()

    def dataset(self):
        return self.chatbot.storage.gets_dataset()

    def save(self,dataset):
        self.chatbot.storage.dataset = dataset

    def reply(self,message):
        try:
            statement = self.chatbot.get_response(message)
            if statement.confidence == 0:
                res = self.chatbot.storage.messages["UNKNOWN"]
                res = re.sub(r"~uname~",self.chatbot.storage.uname,res)
            else:
                res = str(statement)
            res = res.split("\n")
        except exceptions.UnAuthenticated:
            res = ["You are not Authenticated.","Please Login to the website."]
        except Exception as e:
            print(e)
            res = ["Sorry, Something really bad happend!"]
        return res

    @classmethod
    def intro(cls,key,uid='',uname='',channel:Channel=Channel.Web,auth=None)->list:
        from chatbot.core.models import Chatbot as ChatbotModel
        
        if channel in Channel and channel != Channel.Web:
            chatbot = ChatbotModel.objects.get(**{"{}_key".format(channel.value.lower()):key})
        else:
            chatbot = ChatbotModel.objects.get(name = key)
        try:
            if uid:
                if channel!=Channel.Web:
                    uid = Decrypt(uid).substitution.base64urlstrip.removestrstart()
                
                _auth = chatbot.auth.get(uid=uid)
                uname = _auth.uname if _auth.uname else uname

                if channel!=Channel.Web and auth:
                    if not _auth.uname:
                        auth["uname"] = uname
                    _auth.update(**auth)
        except Exception as e: print(e)
        
        intro = chatbot.messages["INTRO"]
        intro = re.sub(r"~uname~",uname,intro)
        return intro.split("\n")

