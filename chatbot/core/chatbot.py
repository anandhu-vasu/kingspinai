from chatbot.core.bots import KingspinAI
from chatbot.core.trainers import SophisticatedTrainer

class ChatBot:
    
    def __init__(self):
        self._chatbot = KingspinAI
        self._name = self._chatbot.name

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

    def reponse(text):
        print(KingspinAI.get_response(text))