from core.bots import KingspinAI
from chatterbot.trainers import ChatterBotCorpusTrainer

class ChatBot:
    def train():
        trainer = ChatterBotCorpusTrainer(KingspinAI)
        trainer.train("./core/data/")
    def reponse(text):
        print(KingspinAI.get_response(text))