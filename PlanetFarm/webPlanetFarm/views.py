from django.shortcuts import render
from .models import Animal, AnimalType, PlanetFarm
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re

texts = ''
my_farm = PlanetFarm(5, 8, 10)


def train():
    chatbot = ChatBot('my_bot')
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        "chatterbot.corpus.english"
    )
    return chatbot


chatbot = train()


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
    print(my_farm.toString())
    print(my_farm.animals)
    return render(request, 'home.html', {'tiles': my_farm.tiles, 'texts': texts})


def reset():
    global texts
    texts = 'Welcome to Planet Farm! Try to enter a sentence below.\n'


def process(text):
    answer = regex_parser(text)
    if answer:
        return answer + "\n"
    global chatbot
    response = chatbot.get_response(text)
    return str(response) + "\n"


def regex_parser(text):
    text = text.lower()
    print([val.value for val in (AnimalType)])
    animal_strings = [val.value for val in (AnimalType)]
    animal = re.search("|".join(animal_strings), text)
    if(animal):
        new_animal = Animal(animal.group())
        my_farm.add_animal(new_animal, True)
        print(new_animal.toString())
        return "animal exists"
