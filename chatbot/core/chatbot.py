from chatterbot import ChatBot as Bot
from chatbot.core.config import CHATBOT_OPTIONS
from chatbot.core.trainers import SophisticatedTrainer
class ChatBot:
    def __init__(self,name,telegram=False):
        from chatbot.core.models import Chatbot as ChatbotModel
        if telegram:
            self.name = ChatbotModel.objects.get(telegram_key=name).name
        else:
            self.name = name
        self.chatbot = Bot(
            name = self.name,
            botkey = self.name,
            **CHATBOT_OPTIONS
        )

    def train(self):
        self.chatbot.storage.drop()
        trainer = SophisticatedTrainer(self.chatbot)
        trainer.train()

    def dataset(self):
        return self.chatbot.storage.gets_dataset()

    def save(self,dataset):
        self.chatbot.storage.dataset = dataset

    def reply(self,message):
        try:
            res = str(self.chatbot.get_response(message)).split("\n")
        except:
            res = ["Sorry, Something really bad happend!"]
        return res