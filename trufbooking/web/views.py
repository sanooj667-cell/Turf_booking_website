from django.shortcuts import render, get_object_or_404
from .models import Sports_Category, Turf

# Create your views here.

def index(request):
    categories = Sports_Category.objects.all()
    turf = Turf.objects.all()
    context = {
        "categories" : categories,
        "turf" : turf
    }
    return render(request,"web/index.html", context=context)

def single_turf(request,id):
    turf = Turf.objects.get(id=id)
    context = {
        "turf" : turf
    }

    return render(request, "web/single_turf.html", context=context)


def login(request):
    return render(request,"web/login.html")

def register(request):
    return render(request,"web/register.html")
