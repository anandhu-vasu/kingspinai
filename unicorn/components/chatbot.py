from django_unicorn.components import UnicornView
from core.chatbot import ChatBot


class ChatbotView(UnicornView):
    def train(self):
        ChatBot.train()
        ChatBot.reponse("Where are you")