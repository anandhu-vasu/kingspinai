from django_unicorn.components import UnicornView, PollUpdate
from convobot.convobot import Convobot
from convobot import exceptions
from convobot.exceptions import *


class ConsoleActionbarView(UnicornView):
    corpus = ""
    name = ""
    _chatbot = None
    is_training = False
    is_saving = False
    is_dataset_ready = False

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        try:
            self.name = kwargs.get('name')
            if not self._chatbot:
                self._chatbot = Convobot(key=self.name)
                self.corpus = self._chatbot.dataset()
                self.is_dataset_ready = self._chatbot.is_dataset_ready
                
            print("chatbot", "initialized")
        except Exception as e:
            print(e)
            self.call("Toast", "Error!", "Something Went Wrong.", "error")
            
            
    def mount(self):
        self.update_training_status()

    def train(self):
        try:
            if self._chatbot.training_status == 202:
                self.is_training = True
                self.call("Toast", "Training Already Started", "", "warning")
            else:
                self._chatbot.train()
                self.is_training = True
                self.call("Toast", "Training Started", "", "success")
        except exceptions.EmptyTrainingDataError:
            self.call("Toast", "Training Failed!",
                      "Dataset is Empty.", "error")
        except exceptions.LTSUnavailableError:
            self.call("Toast", "LTS Unavailable",
                      "", "error")
        except Exception as e:
            print(e)
            self.call("Toast", "Training Failed!",
                      "Something Went Wrong.", "error")
        # else:
        #     self.call("swal", "Training Completed!",
        #               "Your Bot is ready to go.", "success")
        finally:
            self.call("refreshConsole", self.corpus)
            
        if self.is_training:
            return PollUpdate(timing=5000, disable=False, method="update_training_status")

    def save(self, corpus):
        try:
            if not self._chatbot:
                self._chatbot = Convobot(key=self.name)
            self._chatbot.save(corpus)
            self.corpus = corpus
            self.call("Toast", "Training Data Saved!", "", "success")
        except exceptions.InvalidTrainingDataError:
            self.call("Toast", "Saving Failed!",
                      "Invalid Training Data", "error")
        except exceptions.LTSUnavailableError:
            self.call("Toast", "LTS Unavailable",
                      "No Data Loss But, Try Again Later Before Training!", "error")
        except Exception as e:
            print(e)
            self.call("Toast", "Saving Failed!",
                      "Something Went Wrong.", "error")
        finally:
            self.is_dataset_ready = self._chatbot.is_dataset_ready
            self.call("refreshConsole", self.corpus)

    def update_training_status(self):
        training_status = self._chatbot.training_status
        if training_status == 200:
            self.is_training = False
            self.call("swal", "Training Completed!",
                      "Your Bot is ready to go.", "success")
        elif training_status == 404:
            self.is_training = False
            self.call("Toast", "Training Failed!",
                      "Dataset is Empty.", "error")
        elif training_status == 500:
            self.is_training = False
            self.call("Toast", "Training Failed!",
                      "Something Went Wrong.", "error")
        elif training_status == 202:
            self.is_training = True
        else:
            self.is_training=False
        self.call("train_poll_update")
        if self.is_training:    
            return PollUpdate(timing=5000, disable=False, method="update_training_status")
        else:    
            return PollUpdate(timing=5000, disable=True, method="update_training_status")
            
        
