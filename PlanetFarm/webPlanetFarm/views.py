from django.shortcuts import render
from .models import Animal, AnimalType, PlanetFarm
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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
    return render(request, 'home.html', {'tiles': my_farm.values, 'texts': texts})


def test(request):
    global texts
    if request.method == 'POST':
        text_input = request.POST['text_input']
        if text_input != '':
            texts += '> ' + text_input + '\n'
            texts += process(text_input)
    print(my_farm.toString())
    print(my_farm.animals)
    my_farm.update()
    return render(request, 'home.html', {'tiles': my_farm.values, 'texts': texts})


def reset():
    global texts
    texts = 'Welcome to Planet Farm! Try to enter a sentence below.\n'
    global my_farm
    my_farm = PlanetFarm(5, 8, 10)


def process(text):
    answer = regex_parser(tokenize(text))
    if answer:
        return answer + "\n"
    global chatbot
    response = chatbot.get_response(text)
    return str(response) + "\n"


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if (word not in stopwords.words()) or word == 'up' or word == 'down']
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    print(tokens)
    return tokens


def regex_parser(text):
    animal_strings = ['wolf', 'sheep', 'rabbit', 'snake', 'eagle']
    add_strings = ['add', 'create', 'creates', 'creating', 'adding',
                   'generates', 'generating', 'generate', 'generated',
                   'created']
    fence_strings = ['fence', 'wall']
    eat_strings = ['eat', 'eating', 'eats', 'hunt', 'hunting', 'ate', 'get', 'getting']
    herbivores = ['sheep', 'rabbit']
    food_chain = {
        'wolf': ['sheep'],
        'eagle': ['snake', 'rabbit'],
        'snake': ['rabbit']
    }
    food_chain2 = {
        'sheep': ['wolf'],
        'rabbit': ['eagle', 'snake'],
        'snake': ['eagle']
    }

    animals = []
    is_adding = False
    grass = False
    fence = False
    coordinates = []
    x_coordinate = -1
    to_eat = False

    for word in text:
        if word in animal_strings:
            animals.append(word)
        if word in add_strings:
            is_adding = True
        if word == 'grass':
            grass = True
        if word in fence_strings:
            fence = True
        if word.isnumeric():
            if x_coordinate != -1 and 1 <= int(word) <= 5:
                coordinates.append((x_coordinate, int(word)))
                x_coordinate = -1
            elif x_coordinate == -1 and 1 <= int(word) <= 8:
                x_coordinate = int(word)
        if word in eat_strings:
            to_eat = True

    if to_eat:
        result = ""
        current_animals = my_farm.get_animals()
        grasses = my_farm.get_grasses()
        for animal in animals:
            if animal not in current_animals:
                return "The " + animal + " is not in your farm currently"
        animals_in_the_sent = animals.copy()
        while animals:
            animal = animals.pop(0)
            if animal in herbivores:
                if not grasses:
                    result += "The " + animal + " does not find any grass"
                elif not intersection(food_chain2[animal], animals_in_the_sent):
                    result += "The " + animal + " is eating grass"
                continue
            food = intersection(food_chain[animal], current_animals)
            if not food:
                result += "The " + animal + " does not find its prey"
            else:
                result += "The " + animal + " is eating " + food[0]
        return result

    if animals and is_adding:
        result = ""
        for animal in animals:
            new_animal = Animal(animal)
            if coordinates:
                coord = coordinates.pop(0)
                my_farm.add_animal(new_animal, coordinate=coord)
                result += "A " + animal + " has been added to your farm at " + str(coord) + " "
            else:
                my_farm.add_animal(new_animal, True)
                result += "A " + animal + " has been added to your farm at a random position "
        return result

    if grass and is_adding:
        result = ""
        if not coordinates:
            my_farm.add_grass_randomly()
            return "A grass has been added to your farm at a random position "
        for coordinate in coordinates:
            my_farm.add_grass(coordinate)
            result += "A grass has been added to your farm at " + str(coordinate) + " "
        return result

    if fence and is_adding:
        result = ""
        if not coordinates:
            my_farm.add_fence_randomly()
            return "A fence has been added to your farm at a random position "
        for coordinate in coordinates:
            my_farm.add_fence(coordinate)
            result += "A fence has been added to your farm at " + str(coordinate) + " "
        return result


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
