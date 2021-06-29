from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from convobot.convobot import Convobot
from convobot import reply_message
from convobot.models import Chatbot as ChatbotModel
import re


def message_handler(message):
    
    if isinstance(message,reply_message.ReplyText):
        return {
                "mode":"reply",
                "type": 'text',
                "content":message.text,
            }
    elif isinstance(message,reply_message.ReplyMedia):
        return {
                "mode":"reply",
                "type": message.type,
                "content":message.url,
            }
    elif isinstance(message,reply_message.ReplyButtonList):
        return {
                "mode":"reply",
                "type": 'buttons',
                "buttons": [{"label": button.label, "callback": button.callback} for button in message]
            }
    

class WebchatAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = {"messages": []}
        chatbot = Convobot(request.auth.get('chatbot'), uname=request.auth.get(
            'uname', ''), uid=request.auth.get('uid', ''))
        message = request.data.get("message", "")
        response["messages"] = map(
            message_handler, chatbot.reply_messages(text=message))
        return Response(response)

    def get(self, request):
        response = {"messages": []}
        response["messages"] = list(map(message_handler, Convobot.intro_messages(request.auth.get(
            'chatbot'), uname=request.auth.get('uname', ''))))
        print(response)

        return Response(response)




# webchat_message = {
#     "time":"",
#     "mode":"reply"|"sent",
#     "type": 'buttons' | 'text' | 'image' | 'video',
#     "content":'text' | 'src',
#     "buttons": [{"callback":'',"label":''}]
# }
