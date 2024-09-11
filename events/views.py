from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # return a simple response
    return HttpResponse("Welcome to the home page!")
    
# Create your views here.
