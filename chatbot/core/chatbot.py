from chatterbot import ChatBot as Bot
from chatbot.core.bots import CHATBOT_OPTIONS
from chatbot.core.trainers import SophisticatedTrainer

class ChatBot:
    
    def __init__(self,name):
        self._name = name
        self._chatbot = Bot(
            name = self._name,
            botkey = self._name,
            **CHATBOT_OPTIONS
        )

    @property
    def name(self):
        return self._name

    def train(self):
        trainer = SophisticatedTrainer(self._chatbot)
        trainer.train()

    def dataset(self):
        return self._chatbot.storage.gets_dataset()

    def save(self,dataset):
        self._chatbot.storage.dataset = dataset