from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chatbot.core.chatbot import ChatBot
from chatbot.core.models import Chatbot as ChatbotModel
import re

class ChatAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {"messages":[]}
        chatbot = ChatBot(request.auth.get('chatbot'),uname=request.auth.get('uname',''))
        message = request.data.get("message","")
        response["messages"] = chatbot.reply(message=message)
        return Response(response)
    def get(self,request):
        response = {"messages":[]}
        response["messages"] = ChatBot.intro(request.auth.get('chatbot'),uname=request.auth.get('uname',''))
        return Response(response)
        