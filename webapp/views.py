from chatbot.core.facebook_bot.views import get_facebook_page
from chatbot.core.models import Auth
from chatbot.core.utils import Encrypt
from django.shortcuts import get_object_or_404, render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
import json
import telegram
from .models import *
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Avg, Count, Max, Q
from convobot import ConvoChannels
from django.db.models.functions import TruncDay
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import pytz


def index(request):
    return render(request, "index.html", {})


def linguist(request):
    return render(request, "linguist.html", {})


def multi_channel(request):
    return render(request, "multi-channel.html", {})


def voice_enabled(request):
    return render(request, "voice-enabled.html", {})


@login_required
def user(request):
    return redirect("user:dashboard")


@login_required
def dashboard(request):
    return redirect("user:chatbot")


@login_required
def chatbot(request):
    context = {}
    return render(request, 'user/chatbot.html', context)


def datetimetoms(obj):
    if isinstance(obj, datetime):
        return int(round(obj.timestamp() * 1000))


@login_required
def analytics(request):

    analytics = []
    for chatbot in request.user.chatbots.all():
        if chatbot.analytics.exists():
            analysis = {}
            analysis["chatbot_name"] = chatbot.name
            analysis["chatbot_id"] = chatbot.id
            proficiency = round(chatbot.analytics.aggregate(
                Avg('confidence'))['confidence__avg'], 4)
            analysis["proficiency"] = (
                0 if proficiency is None else proficiency)*100
            analysis["response_time"] = chatbot.analytics.aggregate(
                avg=Avg('duration'), max=Max('duration'))
            messagesPerDay = []
            for channel in ConvoChannels:
                data = chatbot.analytics.annotate(x=TruncDay('created_at', tzinfo=pytz.timezone('Asia/Calcutta'))).values(
                    'x').annotate(y=Count('channel', filter=Q(channel=channel.value))).values('x', 'y').order_by('created_at__date')
                #chatbot.analytics.annotate(x=TruncDay('created_at')).values('x').order_by('created_at__date').annotate(y=Count('created_at__date',filter=Q()))
                messagesPerDay.append(
                    {'name': channel.value, 'data': list(data)})

            analysis['messagesPerDay'] = json.dumps(
                messagesPerDay, default=datetimetoms)
            print(analysis)
            analytics.append(analysis)
    context = {"analytics": analytics}
    # print(analytics)
    return render(request, 'user/analytics.html', context)

# analytics[{bot:"",proficiency:100,messagesPerDay: [{name:'Web',data:[{x:Date(),y:}]}] }]
#
#
#
#


@login_required
def console(request, name):
    context = {}
    context['chatbot'] = get_object_or_404(request.user.chatbots, name=name)
    refresh = RefreshToken.for_user(request.user)
    refresh['chatbot'] = name
    refresh['uid'] = "~TEST"
    refresh['uname'] = request.user.name

    context['token'] = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'expiry': str(refresh.access_token["exp"]),
        'auth': Encrypt(refresh['uid']).prependrandom.base64urlstrip.substitution()
    }

    Auth.objects.update_or_create(
        chatbot=context['chatbot'], uid=refresh['uid'], defaults={"uname": refresh['uname']})

    if context['chatbot'].telegram_status and context['chatbot'].telegram_key:
        try:
            context['token']['telegram'] = telegram.Bot(
                token=context['chatbot'].telegram_key).username
        except:
            pass
    if context['chatbot'].facebook_status and context['chatbot'].facebook_key:
        try:
            context['token']['facebook'] = get_facebook_page(
                context['chatbot'].facebook_key)['id']
        except:
            pass

    context['token'] = json.dumps(context['token'])
    context['api_url'] = settings.WEBHOOK_SITE[:-
                                               1] if settings.WEBHOOK_SITE.endswith("/") else settings.WEBHOOK_SITE
    return render(request, 'user/conversation_console.html', context)


def Register(request):
    context = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        context['register_form'] = form
    else:
        form = UserRegistrationForm()
        context['register_form'] = form

    return render(request, "auth/register.html", context)


def login_view(request):
    context = {}
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("user:dashboard")
        else:
            context['login_form'] = form

    else:
        form = UserLoginForm()
        context['login_form'] = form

    return render(request, 'auth/login.html', context)


def logout_view(request):
    logout(request)
    return redirect("login")


def ssl_verify(request):
    f = open('.well-known/pki-validation/30269148F03B43DFA891A56CB33FA529.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")
