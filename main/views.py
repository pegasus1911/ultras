from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to Ultras World</h1>')

def about(request):
    return HttpResponse('<h1>About Ultras World</h1>')
