from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("<h1>Esta é a página de entrada da app boardgamecafe </h1>")

def tempband(request):
    return render(request, 'boardgamecafe/tempband.html')

def tempband(request):
    return render(request, 'boardgamecafe/tempband.html')

def tempband(request):
    return render(request, 'boardgamecafe/tempband.html')
