from django_unicorn.components import UnicornView
from chatbot.core.models import Chatbot
import random

class ChatbotView(UnicornView):
    nid=0
    chatbots=""

    def hydrate(self):
        self.chatbots = self.request.user.chatbots.all()
        self.nid = random.randint(0,9)
        self.call("notifyUI")
    
    def create(self):
        try:
            Chatbot(user=self.request.user).save()
        except Exception as e:
            print(e)
            self.call("Toast", "Chatbot Creation Failed!","","error")

    def delete(self,id):
        try:
            chatbot = self.request.user.chatbots.get(pk=id)
            name = chatbot.name
            chatbot.delete()
            self.call("Toast","Chatbot Deleted!",name,"success")
        except:
            self.call("Toast", "Chatbot Deletion Failed!","","error")
        finally:
            self.call("removeChatbotFinished")