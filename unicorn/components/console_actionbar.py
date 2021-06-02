from django_unicorn.components import UnicornView
from chatbot.core.chatbot import ChatBot
from chatbot.core.exceptions import *

class ConsoleActionbarView(UnicornView):
    corpus=""
    name=""
    _chatbot=None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        try:
            self.name = kwargs.get('name')
            if not self._chatbot:
                self._chatbot = ChatBot(key=self.name)
                self.corpus = self._chatbot.dataset()
            print("chatbot","initialized")
        except Exception as e:
            print(e)
            self.call("Toast", "Error!","Something Went Wrong.","error")
    

    def train(self):
        try:
            self._chatbot.train()
        except EmptyTrainingDataError:
            self.call("Toast", "Training Failed!","Dataset is Empty.","error")
        # except Exception as e:
        #     print(e)
        #     self.call("Toast", "Training Failed!","Something Went Wrong.","error")
        else:
            self.call("swal","Training Completed!","Your Bot is ready to go.","success")
        finally:
            self.call("refreshConsole",self.corpus)

    def save(self,corpus):
        try:
            if not self._chatbot:
                self._chatbot = ChatBot(key=self.name)
            self._chatbot.save(corpus)
            self.corpus = corpus
            self.call("Toast", "Training Data Saved!","","success")
        except:
            self.call("Toast", "Saving Failed!","Something Went Wrong.","error")
        finally:
            self.call("refreshConsole",self.corpus)
            