from django_unicorn.components import UnicornView
from core.chatbot import ChatBot
from core.corpus import Corpus
import json

class ConsoleActionbarView(UnicornView):
    corpus=""

    def mount(self):
        try:
            with open('core/data/data.json') as f:
                self.corpus = f.read()
        except:
            print("Corpus Load Failed: Someting Went Wrong!")
            self.corpus = "[]"

    def train(self):
        ChatBot.train()
        self.call("refreshConsole",self.corpus)
        self.call("swal","Training Completed","Your Bot is ready to go.","success")

    def save(self,corpus):
        self.corpus = corpus
        Corpus.save_to_json(self.corpus)
        self.call("refreshConsole",self.corpus)
        self.call("successToast", "Saved!","Training data saved as data.json")
            