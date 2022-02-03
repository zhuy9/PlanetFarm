from django.shortcuts import render


# Create your views here.
from .models import PlanetFarm


def home(request):
    my_farm = PlanetFarm(5, 8, 10)
    return render(request, 'home.html', {'tiles': my_farm.tiles})
