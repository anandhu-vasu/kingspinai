from convobot.process_response import ProcessResponse


class Response:
    def __init__(self,*args, **kwargs) -> None:
        self.uname = kwargs["uname"]
        self.entities = kwargs.get("entities",None)
        self.values = kwargs.get("values",None)
        self.translate_to = kwargs.get("translate_to",None)
        
class TextResponse(Response):
    def __init__(self,text,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = ProcessResponse(
            self, text).sub_uname.sub_entities.sub_values.translate()
        
class MediaResponse(Response):
    def __init__(self,type,url, *args, **kwargs) -> None:
        self.type = type
        self.url = url
        super().__init__(*args, **kwargs)

class ButtonResponse(Response):
    def __init__(self,statement,callback, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.statement = ProcessResponse(
            self, statement).sub_uname.sub_entities.sub_values.translate()
        self.callback = ProcessResponse(
            self, callback).sub_uname.sub_entities.sub_values.translate()

