from django.shortcuts import render,redirect
from . forms import UserRegistrationForm,UserLoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request,'auth/dash.html')




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
                return redirect("dashboard")
                

        else:
            context['login_form']=form

        
    else:
        form=UserLoginForm()
        context['login_form']=form

    return render(request,'auth/login.html',context)  




def logout_view(request):
     logout(request)
     return redirect("login")   
