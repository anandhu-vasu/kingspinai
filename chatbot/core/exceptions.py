from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status

class ChatbotError(Exception):
    pass

class EmptyTrainingDataError(ChatbotError):
    def __init__(self,message="Provide Sufficient Training Data for Chatbot"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class BotkeyNotFoundError(ChatbotError):
    def __init__(self, message='Botkey not provided as botkey=... in Chatbot instance!'):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message

class ChatbotRequired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('chatbot field required.')
    default_code = 'chatbot_required'
class ChatbotNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Chatbot not found.')
    default_code = 'chatbot_not_found'


class ReplyError(Exception):
    def __init__(self, message="Sorry for the inconvenience.\nSomething really bad happend!"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message

class NonExtractedEntityOnReply(ReplyError):
    def __init__(self, message="Sorry, We can't find enough data"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message
class NonExtractedValueOnReply(ReplyError):
    def __init__(self, message="Sorry, We can't find enough data"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message
class UnAuthenticated(ReplyError):
    def __init__(self, message="You are not Authenticated"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message
class FacebookUserNotFound(ReplyError):
    def __init__(self, message="You are not Authenticated"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message
class FacebookUserNotFound(ReplyError):
    def __init__(self, message="Facebook User Not Found"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message

