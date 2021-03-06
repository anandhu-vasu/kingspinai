from django.conf.urls import url
from django.shortcuts import get_object_or_404, render,redirect
from . forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import detailsSerializer
from rest_framework import serializers

from .models import *


@api_view(['GET'])
def home(request):
    api_urls ={
    #  'List':'/show/',
     'show':'/show/',



        }
    return Response(api_urls)


@api_view(['GET'])

def show(request):
    detail=User.objects.all()
    serializer=detailsSerializer(detail,many=True)
    return Response(serializer.data)


def index(request):
    return render(request,"index.html",{})
    
def demo(request):
    return render(request,'user/conversation_console.html',{})

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

