from django.shortcuts import render
from .models import PlanetFarm
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

texts = ''
my_farm = PlanetFarm(5, 8, 10)


def home(request):
    reset()
    return render(request, 'home.html', {'tiles': my_farm.tiles, 'texts': texts})


def test(request):
    global texts
    if request.method == 'POST':
        text_input = request.POST['text_input']
        if text_input != '':
            texts += '> ' + text_input + '\n'
            texts += process(text_input)
    return render(request, 'home.html', {'tiles': my_farm.tiles, 'texts': texts})


def reset():
    global texts
    texts = 'Welcome to Planet Farm! Try to enter a sentence below.\n'


def process(text):
    chatbot = train()
    response = chatbot.get_response(text)
    return str(response) + "\n"


def train():
    chatbot = ChatBot('my_bot')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        "chatterbot.corpus.english"
    )
    return chatbot
