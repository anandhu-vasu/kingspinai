from django_unicorn.components import UnicornView
from chatbot.core.chatbot import ChatBot
from chatbot.core.corpus import Corpus
from chatbot.core.exceptions import *

class ConsoleActionbarView(UnicornView):
    corpus=""

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.chatbot = ChatBot()

    def mount(self):
        self.corpus = self.chatbot.dataset()

    def train(self):
        try:
            self.chatbot.train()
        except EmptyTrainingDataError:
            self.call("Toast", "Training Failed!","Dataset is Empty.","error")
        except Exception as e:
            print(e)
            self.call("Toast", "Training Failed!","Something Went Wrong.","error")
        else:
            self.call("swal","Training Completed!","Your Bot is ready to go.","success")
        finally:
            self.call("refreshConsole",self.corpus)

    def save(self,corpus):
        try:
            self.chatbot.save(corpus)
            self.corpus = corpus
            self.call("Toast", "Training Data Saved!","","success")
        except:
            self.call("Toast", "Saving Failed!","Something Went Wrong.","error")
        finally:
            self.call("refreshConsole",self.corpus)
            