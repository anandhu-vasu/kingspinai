from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"index.html",{})
def why(request):
    return render(request,"whykingspinai.html",{})
