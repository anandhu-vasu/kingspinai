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