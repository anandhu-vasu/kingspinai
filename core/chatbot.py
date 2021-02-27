from core.bots import KingspinAI
from core.trainer import SophisticatedTrainer
import json
class ChatBot:
    def train():
        trainer = SophisticatedTrainer(KingspinAI)
        try:
            with open('core/data/data.json') as f:
                corpus = json.load(f);
                KingspinAI.storage.drop()
                trainer.train(*corpus)
        except:
            print("Training Failed: Someting Went Wrong!")
    def reponse(text):
        print(KingspinAI.get_response(text))