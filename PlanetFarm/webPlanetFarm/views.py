from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from .models import PlanetFarm


def home(request):
    messages.info(request, 'Hi!')
    my_farm = PlanetFarm(5, 8, 10)
    return render(request, 'home.html', {'tiles': my_farm.tiles})


def test(request):
    my_farm = PlanetFarm(5, 8, 10)
    return render(request, 'home.html', {'tiles': my_farm.tiles})
