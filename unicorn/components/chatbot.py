from django_unicorn.components import UnicornView
from chatbot.core.models import Chatbot,Training
import random

class ChatbotView(UnicornView):
    nid=0
    chatbots=""

    def hydrate(self):
        self.refreshChatbots()
        self.nid = random.randint(0,9)
        self.call("notifyUI")

    def refreshChatbots(self):
        if self.request:
            chatbots = self.request.user.chatbots.values("id","name").all()
            self.chatbots = list(chatbots)

    def create(self):
        try:
            chatbot = Chatbot(user=self.request.user)
            chatbot.save()
            Training(chatbot=chatbot).save()
            self.refreshChatbots()
        except Exception as e:
            print(e)
            self.call("Toast", "Chatbot Creation Failed!","","error")

    def delete(self,id):
        try:
            chatbot = self.request.user.chatbots.get(pk=id)
            name = chatbot.name
            chatbot.delete()
            self.refreshChatbots()
            self.call("Toast","Chatbot Deleted!",name,"success")
        except Exception as e:
            print(e)
            self.call("Toast", "Chatbot Deletion Failed!","","error")
        finally:
            self.call("removeChatbotFinished")