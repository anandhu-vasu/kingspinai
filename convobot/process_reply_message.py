from convobot import constants, exceptions
from textblob import TextBlob
import re

class ProcessReplyMessage:
    
    def __init__(self,response,text:str) -> None:
        self._text = text
        self._response = response
        
    @property
    def text(self)->str:
        return self._text

    def __call__(self) -> str:
        return self._text
    
    @property
    def sub_uname(self):
        self._text = re.sub(constants.RE_UNAME, self._response.uname, self._text)
        return self

    @property
    def sub_entities(self):
        if self._response.entities:
            entities = self._response.entities.copy()
            while True:
                match = re.search(
                    constants.RE_ENTITY, self._text)
                if not match:
                    break
                try:
                    if len(entities[match.group(1)]) > 1:
                        # repetition of same entity in text
                        if self._text.count(f"~{match.group(1)}~") > 1:
                            self._text = re.sub(constants.RE_ENTITY, str(
                                entities[match.group(1)][0]), self._text, 1)
                            del entities[match.group(1)][0]
                        else:
                            self._text = re.sub(constants.RE_ENTITY, ', '.join(
                                map(str, entities[match.group(1)])), self._text, 1)
                    else:
                        self._text = re.sub(constants.RE_ENTITY, str(
                            entities[match.group(1)][0]), self._text, 1)
                except:
                    raise exceptions.UnknownEntityOnReply()

        return self

    @property
    def sub_values(self):
        if self._response.values:
            values = self._response.values.copy()
            while True:
                match = re.search(
                    constants.RE_VALUE, self._text)
                if not match:
                    break
                try:
                    if len(values[match.group(1)]) > 1:
                        # repetition of same value in text
                        if self._text.count(f"~{match.group(1)}~") > 1:
                            self._text = re.sub(constants.RE_VALUE, str(
                                values[match.group(1)][0]), self._text, 1)
                            del values[match.group(1)][0]
                        else:
                            self._text = re.sub(constants.RE_VALUE, ', '.join(
                                map(str, values[match.group(1)])), self._text, 1)
                    else:
                        self._text = re.sub(constants.RE_VALUE, str(
                            values[match.group(1)][0]), self._text, 1)
                    self._text = re.sub(constants.RE_VALUE, str(
                        values[match.group(1)]), self._text, 1)
                except Exception as e:
                    print(e)
                    raise exceptions.UnknownValueOnReply()
        return self
    
    @property
    def translate(self):
        if self._response.translate_to and self._response.translate_to != 'en':
            try:
                self._text = str(TextBlob(self._text).translate(to=self._response.translate_to))
            except:
                pass
        return self
