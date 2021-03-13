from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chatbot.core.chatbot import ChatBot

class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Success'}
        print(request.data)
        return Response(content)

class ChatAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {"messages":[]}
        chatbot = ChatBot(request.auth.get('chatbot'))
        message = request.data.get("message","")
        response["messages"].append(chatbot.reply(message=message))
        return Response(response)
    def get(self,request):
        response = {"messages":[]}
        response["messages"].append("Hello! "+request.auth.get('uname',''))
        response["messages"].append("How can I help you!")
        return Response(response)
        