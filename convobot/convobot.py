
from crypt import Encrypt
from convobot.reply_message import ReplyMessage, generate_reply_messages
from typing import List
from convobot.response import Response
from convobot.convo_channels import ConvoChannels
from chatbot.core.utils import Decrypt
from . import exceptions
import chatbot
from chatterbot import ChatBot as Bot
from chatbot.core.config import CHATBOT_OPTIONS
from chatbot.core.trainers import SophisticatedTrainer

import re
from textblob import TextBlob
import speech_recognition as sr
from pyffmpeg import FFmpeg
import os
import time
import datetime
import json
import requests

from .models import Chatbot as ChatbotModel, Analytics
from .schemas import Messages, Reply, Statement, Authorization, Corpus
from convobot import constants

from convobot import models
from django.conf import settings


class Convobot:
    
    def __init__(self, key, channel: ConvoChannels = ConvoChannels.WEB, uid: str = '', uname='', auth=None) -> None:

        # from chatbot.core.models import Chatbot as ChatbotModel

        self.is_auth:bool = False
        self.uid:str = uid
        self.channel = channel
        
        if channel in ConvoChannels and channel != ConvoChannels.WEB:
            chatbot = ChatbotModel.objects.get(
                **{"{}_key".format(channel.name.lower()): key})
        else:
            chatbot:ChatbotModel = ChatbotModel.objects.get(name=key)
            
        self.name:str = chatbot.name
        self.chatbot_id:int = chatbot.id
        self.data_url = chatbot.data_url
        self.data_key = chatbot.data_key
        self.messages = chatbot.messages
        
        self.LTS:models.LTS = chatbot.LTS
        self.isLTS200 = self.hello_lts()
        
        if uid:
            try:
                _auth = chatbot.auth.get(uid=uid)
                self.is_auth = True
                uname = _auth.uname if _auth.uname else uname

                if channel != ConvoChannels.WEB:
                    if auth:
                        _auth.update(**auth, uname=uname)
            except:
                pass
        elif auth and channel != ConvoChannels.WEB:
            try:
                _auth = chatbot.auth.get(**auth)
                self.is_auth = True
                uname = _auth.uname if _auth.uname else uname
            except:
                pass
        # TODO: add extra fields for auth table checking if user is authenticated
        
        self.uname = uname
        
    @property
    def _headers(self) -> dict: return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Token": self.token
    }

    def dataset(self):
        dataset = self.LTS.dataset
        if not dataset:
            return "[]"
        return json.dumps(dataset, separators=(',', ':'))

    def save(self, dataset):#throws exception
        try:
            corpus = Corpus(dataset=json.loads())
        except:
            raise exceptions.InvalidTrainingDataError()
        self.LTS.dataset = corpus.dict()['dataset']
        if self.isLTS200:
            res = requests.post(f"{self.LTS.url}/dataset/{self.LTS.botsign}",data=corpus.json(),headers=self._headers)
            if res.status_code == 200:
                return
        raise exceptions.LTSUnavailableError()
        

    def train(self):
        if self.isLTS200:
            callback_url = settings.WEBHOOK_URL.format(
                webhook_name='training_status',
                bot_token=Encrypt(self.LTS.botsign).base64urlstrip.substitution.prependrandom()
            )
            res = requests.post(
                f"{self.LTS.url}/train/{self.LTS.botsign}?callback_url={callback_url}", headers=self._headers)
            
            if res.status_code == 202:
                self.LTS.training_status = 202
                self.LTS.save()
                return True
        
        return False 
    
    def reply_messages(self,text) -> List[ReplyMessage]:
        if self.isLTS200:
            start = time.time_ns()//1e6
            confidence:int = 0
            try:
                
                blob = TextBlob(text)
                try:
                    lang = blob.detect_language()
                    if lang != 'en':
                        blob = blob.translate(to='en')
                except:
                    lang = 'en'
                    
                data = Statement(text=text, uid=self.uid, is_auth=self.is_auth,
                                 data_url=self.data_url, data_key=self.data_key).json()
                res = requests.post(f"{self.LTS.url}/reply/{self.LTS.botsign}",
                                    data=data, headers=self._headers)
                reply_messages = None
                if res.status_code == 200:
                    reply = Reply(**res.json())
                    confidence = reply.confidence
                    reply_messages = generate_reply_messages(
                        reply=reply, uname=self.uname, translate_to=lang, messages=Messages(**self.messages))
                    if confidence:
                        end = time.time_ns()//1e6
                        Analytics.objects.create(chatbot_id=self.chatbot_id, duration=int(
                            end-start), channel=self.channel.name, confidence=confidence)
                    return reply_messages
            except:
                pass
        reply_messages = generate_reply_messages(
            reply=Reply(texts=["Sorry, Something really bad happend!"]), uname=self.uname, translate_to=lang, messages=Messages(**self.messages))
        return reply_messages
    
    def change_token(self,token):
        if self.isLTS200:
            try:
                data = Authorization(token=token).json()
                res = requests.post(f"{self.LTS.url}/token",
                                    data=data, headers=self._headers)
                if res.status_code == 200:
                    self.LTS.token = token
                    self.LTS.save()
                    return True
            except:
                pass
        else:
            return False
        
        
    def hello_lts(self):
        if self.LTS.url and self.LTS.token:
            res = requests.get(f"{self.LTS.url}/hello",headers=self._headers)
            if res.status_code == 200:
                return True
        return False
        
    @classmethod
    def intro_messages(cls, key, uid='', uname='', channel: ConvoChannels = ConvoChannels.WEB, auth=None) -> List[ReplyMessage]:
        
        if channel in ConvoChannels and channel != ConvoChannels.WEB:
            chatbot = ChatbotModel.objects.get(
                **{"{}_key".format(channel.name.lower()): key})
        else:
            chatbot: ChatbotModel = ChatbotModel.objects.get(name=key)
        
        try:
            if uid:
                if channel != ConvoChannels.WEB:
                    uid = Decrypt(
                        uid).substitution.base64urlstrip.removestrstart()

                _auth = chatbot.auth.get(uid=uid)
                uname = _auth.uname if _auth.uname else uname

                if channel != ConvoChannels.WEB and auth:
                    if not _auth.uname:
                        auth["uname"] = uname
                    _auth.update(**auth)
        except Exception as e:
            print(e)
            
        return generate_reply_messages(None, uname, messages = Messages(**chatbot.messages))

    def replyFromVoice(self, voice):
        r = sr.Recognizer()
        ff = FFmpeg()
        voice_wav = ff.convert(voice, voice.rsplit('.', 1)[0] + '.wav')
        audio_file = sr.AudioFile(voice_wav)
        with audio_file as source:
            audio = r.record(source)
        try:
            result = r.recognize_google(audio)
            print(result)
            res = self.reply(str(result))
        except sr.RequestError:

            # API was unreachable or unresponsive
            res = ["Sorry, We are unable to process your voice"]
        except sr.UnknownValueError:
            # speech was unintelligible
            res = self.chatbot.storage.messages["UNKNOWN"].split("\n")

        if os.path.exists(voice):
            os.remove(voice)
        if os.path.exists(voice_wav):
            os.remove(voice_wav)
        return res
    
