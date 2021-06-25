from pydantic import BaseModel, root_validator
from typing import Dict, List, Optional, Union
from . import constants

class Messages(BaseModel):
    UNKNOWN: Union[str, List]
    INTRO: Union[str, List]

    @root_validator
    def convert(cls, values):
        for key in values:
            if isinstance(values[key], str):
                values[key] = values[key].split(constants.MESSAGE_SEPARATOR)
        return values
    

class Statement(BaseModel):
    text: str
    uid: str
    is_auth: bool
    data_url: Optional[str]
    data_key: Optional[str]


# dataset
class Button(BaseModel):
    label: str
    callback: str


class Conversation(BaseModel):
    intent: str
    auth: bool
    data_fetch: bool
    entities: List[str]
    statements: List[str]
    responses: List[str]
    buttons: List[Button]


class Story(BaseModel):
    name: str
    categories: List[str]
    conversations: List[Conversation]


class Corpus(BaseModel):
    dataset: List[Story]
#


class Statement(BaseModel):
    text: str
    uid: str
    is_auth: bool
    data_url: Optional[str]
    data_key: Optional[str]


class Authorization(BaseModel):
    token: str


""" Response to Convobot """


class Param(BaseModel):
    entities: Optional[Dict[str, List[str]]]
    values: Optional[Dict[str, List[str]]]
    texts: Optional[List[str]]


class Reply(BaseModel):
    confidence: float = 0
    texts: Optional[List[str]]
    params: Optional[List[Param]]
    buttons: Optional[List[Button]]
#
