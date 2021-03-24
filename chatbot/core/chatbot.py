from chatterbot import ChatBot as Bot
from chatbot.core.config import CHATBOT_OPTIONS
from chatbot.core.trainers import SophisticatedTrainer
import re
from enum import Enum

class BotType(str,Enum):
    WEB = "Web"
    TELEGRAM = "Telegram"


class ChatBot:
    def __init__(self,name,bot_type:BotType=BotType.WEB,uname=''):
        from chatbot.core.models import Chatbot as ChatbotModel
        if bot_type == BotType.TELEGRAM:
            self.name = ChatbotModel.objects.get(telegram_key=name).name
        else:
            self.name = name
        self.uname = uname
        self.chatbot = Bot(
            name = self.name,
            botkey = self.name,
            uname= self.uname,
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
        except:
            res = ["Sorry, Something really bad happend!"]
        return res

    @classmethod
    def intro(cls,name,uname='',bot_type:BotType=BotType.WEB)->list:
        from chatbot.core.models import Chatbot as ChatbotModel
        if bot_type == BotType.TELEGRAM:
            intro = ChatbotModel.objects.only("messages").get(telegram_key=name).messages["INTRO"]
        else:
            intro = ChatbotModel.objects.only("messages").get(name=name).messages["INTRO"]
        intro = re.sub(r"~uname~",uname,intro)
        return intro.split("\n")

