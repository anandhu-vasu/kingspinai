from django_unicorn.components import UnicornView
from chatbot.core.chatbot import ChatBot
from chatbot.core.exceptions import *

class ConsoleActionbarView(UnicornView):
    corpus=""
    name=""
    _chatbot=""

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name')
        self._chatbot = ChatBot(name=self.name)
        print("chatbot","initialized")

    def mount(self):
        print("dataset loading")
        self.corpus = self._chatbot.dataset()
        print("dataset loaded")

    def train(self):
        try:
            self._chatbot.train()
        except EmptyTrainingDataError:
            self.call("Toast", "Training Failed!","Dataset is Empty.","error")
        except Exception as e:
            self.call("Toast", "Training Failed!","Something Went Wrong.","error")
        else:
            self.call("swal","Training Completed!","Your Bot is ready to go.","success")
        finally:
            self.call("refreshConsole",self.corpus)

    def save(self,corpus):
        try:
            self._chatbot.save(corpus)
            self.corpus = corpus
            self.call("Toast", "Training Data Saved!","","success")
        except:
            self.call("Toast", "Saving Failed!","Something Went Wrong.","error")
        finally:
            self.call("refreshConsole",self.corpus)
            