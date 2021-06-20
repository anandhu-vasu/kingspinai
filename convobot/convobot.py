
from typing import List
from convobot.response import Response
from convobot.convo_channels import ConvoChannels
from chatbot.core.utils import Decrypt
from chatbot.core import exceptions
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

from .models import Chatbot as ChatbotModel
from convobot import constants



    
class Convobot:
    def __init__(self, key, channel: ConvoChannels = ConvoChannels.WEB, uid: str = '', uname='', auth=None) -> None:

        # from chatbot.core.models import Chatbot as ChatbotModel

        self.is_auth = False
        self.uid = uid
        self.channel = channel
        
        if channel in ConvoChannels and channel != ConvoChannels.WEB:
            chatbot = ChatbotModel.objects.get(
                **{"{}_key".format(channel.name.lower()): key})
        else:
            chatbot = ChatbotModel.objects.get(name=key)
            
        self.name = chatbot.name
        self.chatbot_id = chatbot.id
        
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
        
    def train(self):
        # trainer = SophisticatedTrainer(self.chatbot)
        # trainer.train()
        
        # TODO: Add api to train chatbot remotely
        pass

    def dataset(self):
        # return self.chatbot.storage.gets_dataset()
        # TODO: Add api to fetch dataset remotely
        pass

    def save(self, dataset):
        # self.chatbot.storage.dataset = dataset
        # TODO: Add api to save dataset to remote location
        pass
        
    def get_response(self) -> List:
        # TODO: Add api to receive response remotely
        pass
    
    def reply(self, message):
        start = time.time_ns()//1e6
        confidence = None
        try:
            blob = TextBlob(message)
            try:
                lang = blob.detect_language()
                if lang != 'en':
                    blob = blob.translate(to='en')
            except:
                lang = 'en'

            statement = self.chatbot.get_response(str(blob))
            if statement.confidence == 0:
                res = self.chatbot.storage.messages["UNKNOWN"]
                res = re.sub(constants.RE_UNAME, self.chatbot.storage.uname, res)
            else:
                confidence = statement.confidence
                res = str(statement)
                res = re.sub(constants.RE_MEDIA, r'\n\g<2>\n', res)  # wrap media files
            res = res.split("\n")

            # def buttoninze(btnstr):
            #     m = re.match(reg_media, btnstr);
            #     if m: return {"type": "button", "label":m.groups(0) if lang == 'en' else TextBlob(m.groups(0)).translate(to=lang), "callback": m.groups(1) if lang == 'en' else TextBlob(m.groups(1)).translate(to=lang)}
            #     else: return m

            # res = list(map(buttoninze,res))
            def translate(text):
                try:
                    return str(TextBlob(text).translate(to=lang))
                except:
                    return text

            def translateButton(btn):
                return btn if lang == 'en' else {"type": "button", "label": translate(btn["label"]), "callback": translate(btn["callback"])}
                # return {"type": "button", "label":btn["label"] if lang == 'en' else TextBlob(btn["label"]).translate(to=lang), "callback": btn["callback"] if lang == 'en' else TextBlob(btn["callback"]).translate(to=lang)}

            def resmapper(i):
                m = re.match(constants.RE_BUTTON, i)
                if m:
                    return {"type": "buttons", "buttons": list(map(translateButton, json.loads(m.groups()[0])))}
                return i if (isinstance(i, dict) or lang == 'en' or re.match(constants.RE_MEDIA, i)) else translate(i)

            res = list(map(resmapper, res))

            # res = [i if ( isinstance(i,dict) or lang == 'en' or re.match(reg_media,i)) else str(TextBlob(i).translate(to=lang)) for i in res if i]
        except exceptions.UnAuthenticated:
            res = ["You are not Authenticated.",
                   "Please Login to the website."]
        except Exception as e:
            print(e)
            res = ["Sorry, Something really bad happend!"]
        if confidence:
            end = time.time_ns()//1e6
            from chatbot.core.models import Analytics
            Analytics.objects.create(chatbot_id=self.chatbot_id, duration=int(
                end-start), channel=self.channel.name, confidence=confidence)
        return res

    @classmethod
    def intro(cls, key, uid='', uname='', channel: ConvoChannels = ConvoChannels.WEB, auth=None) -> list:
        from chatbot.core.models import Chatbot as ChatbotModel

        if channel in ConvoChannels and channel != ConvoChannels.WEB:
            chatbot = ChatbotModel.objects.get(
                **{"{}_key".format(channel.value.lower()): key})
        else:
            chatbot = ChatbotModel.objects.get(name=key)
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

        intro = chatbot.messages["INTRO"]
        intro = re.sub(r"~uname~", uname, intro)
        intro = re.sub(constants.RE_MEDIA, r'\n\g<2>\n', intro)  # wrap media files
        return intro.split("\n")

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
    
