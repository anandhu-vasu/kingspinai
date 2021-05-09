from chatbot.core.facebook_bot.views import get_facebook_page
from chatbot.core.models import Auth
from chatbot.core.utils import Encrypt
from django.shortcuts import get_object_or_404, render,redirect
from . forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
import json,telegram
from .models import *
from django.http import HttpResponse


def index(request):
    return render(request,"index.html",{})
    
@login_required
def user(request):
    return redirect("user:dashboard")

@login_required
def dashboard(request):
    return redirect("user:chatbot")

@login_required
def chatbot(request):
    context = {}
    return render(request,'user/chatbot.html',context)

@login_required
def console(request,name):
    context = {}
    context['chatbot'] = get_object_or_404(request.user.chatbots,name=name)
    refresh = RefreshToken.for_user(request.user)
    refresh['chatbot'] = name
    refresh['uid'] = "~TEST"
    refresh['uname'] = request.user.name

    context['token'] = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'expiry': str(refresh.access_token["exp"]),
        'auth' : Encrypt(refresh['uid']).prependrandom.base64urlstrip.substitution()
    }

    Auth.objects.update_or_create(chatbot=context['chatbot'],uid=refresh['uid'],defaults={"uname":refresh['uname']})

    if context['chatbot'].telegram_status and context['chatbot'].telegram_key:
        try:
            context['token']['telegram'] = telegram.Bot(token=context['chatbot'].telegram_key).username
        except:
            pass
    if context['chatbot'].facebook_status and context['chatbot'].facebook_key:
        try:
            context['token']['facebook'] = get_facebook_page(context['chatbot'].facebook_key)['id']
        except:
            pass

    context['token'] = json.dumps(context['token'])
    return render(request,'user/conversation_console.html',context)

def Register(request):
    context={}
    if request.POST:
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        context['register_form']=form 
    else:
        form=UserRegistrationForm()
        context['register_form']=form 


    return render(request,"auth/register.html",context)



def login_view(request):
    context={}
    if request.POST:
        form=UserLoginForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(request,email=email,password=password)

            if user is not None:
                login(request,user)
                return redirect("user:dashboard")
        else:
            context['login_form']=form

        
    else:
        form=UserLoginForm()
        context['login_form']=form

    return render(request,'auth/login.html',context)  

def logout_view(request):
     logout(request)
     return redirect("login")   

def ssl_verify(request):
    f = open('.well-known/pki-validation/30269148F03B43DFA891A56CB33FA529.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")