from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from .models import PlanetFarm

texts = ''
my_farm = PlanetFarm(5, 8, 10)


def home(request):
    global texts
    texts = 'Welcome to Planet Farm! Try to enter a sentence below.\n'
    return render(request, 'home.html', {'tiles': my_farm.tiles, 'texts': texts})


def test(request):
    global texts
    if request.method == 'POST':
        text_input = request.POST['text_input']
        if text_input != '':
            texts += text_input + '\n'
            texts += process(text_input)
    return render(request, 'home.html', {'tiles': my_farm.tiles, 'texts': texts})


def process(text):
    return 'hello\n'
