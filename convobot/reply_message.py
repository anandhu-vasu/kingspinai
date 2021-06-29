import re
from convobot import constants
from typing import List, Union
from convobot.schemas import Button, Messages, Reply
from convobot.process_reply_message import ProcessReplyMessage


class ReplyMessage:
    def __init__(self,**kwargs) -> None:
        self.uname = kwargs.get("uname",'')
        self.entities = kwargs.get("entities",None)
        self.values = kwargs.get("values",None)
        self.translate_to = kwargs.get("translate_to",None)
        
class ReplyText(ReplyMessage):
    def __init__(self,text,**kwargs) -> None:
        super().__init__(**kwargs)
        self.text = ProcessReplyMessage(
            self, text).sub_uname.sub_entities.sub_values.translate()

class ReplyMedia(ReplyMessage):
    def __init__(self,type,url, **kwargs) -> None:
        self.type = type
        self.url = url
        super().__init__(**kwargs)

class ReplyButton(ReplyMessage):
    def __init__(self,label,callback, **kwargs) -> None:
        super().__init__(**kwargs)
        self.label = ProcessReplyMessage(
            self, label).sub_uname.sub_entities.sub_values.translate()
        self.callback = ProcessReplyMessage(
            self, callback).sub_uname.sub_entities.sub_values()
        
class ReplyButtonList(list):
    def __init__(self, buttons: List[Button], uname:str, values=[], entities=[], translate_to:str=None, ** kwargs):
        super(ReplyButtonList, self).__init__([ReplyButton(label=button.label, callback=button.callback, uname=uname, values=values, entities=entities, translate_to=translate_to) for button in buttons], **kwargs)
    
        

def generate_reply_messages(reply: Reply, uname, translate_to=None, messages: Messages = None) -> List[Union[ReplyText, ReplyMedia, ReplyButtonList]]:
    reply_messages = []
    if reply:
        if reply.confidence == 0:
            if reply.texts:
                for text in reply.texts:
                    reply_messages.append(ReplyText(
                        text=text, uname=uname, translate_to=translate_to))
            elif messages:
                if messages.UNKNOWN:
                    for text in messages.UNKNOWN:
                        reply_messages.append(ReplyText(
                            text=text, uname=uname, translate_to=translate_to))
        else:
            if reply.params:
                for param in reply.params:
                    texts = []
                    if param.texts:
                        texts = param.texts
                    elif reply.texts:
                        texts = reply.texts
                        
                    if texts:
                        for text in texts:
                            try:
                                text = ProcessReplyMessage(
                                    ReplyMessage(values=param.values),text).sub_values()
                            except Exception as e:
                                print(e)
                            
                            while True:
                                match = re.search(constants.RE_MEDIA, text)
                                
                                if match:
                                    if (pretext := text[:match.span()[0]]) and not pretext.isspace():
                                        reply_messages.append(ReplyText(
                                            text=pretext, uname=uname, entities=param.entities, translate_to=translate_to))

                                    reply_messages.append(ReplyMedia(
                                        type=match.groups()[1], url=match.groups()[2]))
                                    
                                    text = text[match.span()[1]:]
                                else:
                                    if text and not text.isspace():
                                        reply_messages.append(ReplyText(
                                            text=text, uname=uname, entities=param.entities, translate_to=translate_to))
                                    break
                    
                    if reply.buttons:
                        reply_messages.append(ReplyButtonList(
                            buttons=reply.buttons, uname=uname, values=param.values, entities=param.entities, translate_to=translate_to))
    elif messages and messages.INTRO:
        for text in messages.INTRO:
            reply_messages.append(ReplyText(
                text=text, uname=uname, translate_to=translate_to))
        
    return reply_messages
