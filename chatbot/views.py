from django.shortcuts import render,redirect
import datetime 
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

from .serializers import *


from.models import *


@api_view(['GET'])
def home(request):
    api_urls ={
     'List':'/show/',
     'view':'/view/',



        }
    return Response(api_urls)




@api_view(['GET'])

def show(request):
    detail=UserData.objects.all()
    serializer=detailsSerializer(detail,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def usercreate(request):
    serializer=detailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)




def Register(request):
   
    form=CreateUserForm()
    
    if request.method=='POST':
        pass1=request.POST["password"]
        pass2=request.POST["password2"]
        name=request.POST["name"]
        if UserData.objects.filter(name=name,password=pass1) :
            return HttpResponse("<script>alert('User is Existing');window.location.href=''</script>")
        if pass1 != pass2:
            messages.warning(request,'Password is Incorrect')
        else:
            form=CreateUserForm(request.POST)
            if form.is_valid():
                 form.save()
            # user=form.cleaned_data.get('username')
            # messages.success(request,'Account was created for ' +  user)
            return redirect('login')
    context={'form':form}
           
    return render(request,'auth/register.html',context)








def Login(request):
    if request.method=='POST':
        username=  request.POST.get('name')
        password= request.POST.get('password')
        if UserData.objects.filter(name=username,password=password) :
            return HttpResponse("<script>alert('Welcome user');window.location.href='index'</script>")
        else:
            messages.warning(request,"Username or Password is Incorrect")    
    return render(request,"auth/login.html")



 
def Logout(request):
    logout(request)
    return redirect('login')
   
def Show(request):
    return render(request,'dashboard.html')  
# Create your views here.

def index(request):
    return render(request,"index.html",{})
    
def console(request):
    return render(request,'user/conversation_console.html',{})
