from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from crypt.crypt import Decrypt
from convobot.models import LTS
import json

class TrainingStatusWebhook(generic.View):
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        if 'bot_token' in kwargs:
            kwargs['bot_token'] = Decrypt(
                kwargs['bot_token']).removestrstart.substitution.base64urlstrip()
        return generic.View.dispatch(self, *args, **kwargs)

    def post(self, request, bot_token):
        try:
            req = json.loads(request.body)
            if req['statuscode'] in [200,404,500]:
                lts:LTS = LTS.objects.filter(botsig=bot_token).first()
                lts.training_status = req['statuscode']
                lts.save()
        except:
            lts: LTS = LTS.objects.filter(botsig=bot_token).first()
            lts.training_status = 500
            lts.save()
class LTSRegistrationWebhook(generic.View):
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        if 'bot_token' in kwargs:
            kwargs['bot_token'] = Decrypt(
                kwargs['bot_token']).removestrstart.substitution.base64urlstrip()
        return generic.View.dispatch(self, *args, **kwargs)

    def post(self, request, bot_token):
        try:
            lts: LTS = LTS.objects.filter(botsig=bot_token).first()
            if lts.validation_token == request.body:
                HttpResponse(status=200)
        except:
            pass
            
        return HttpResponse(403)
