from django.db import models


# Create your models here.
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class PlanetFarm:
    def __init__(self, rows, cols, tile_size):
        self.rows = rows
        self.cols = cols
        self.tiles = [[Tile(j * tile_size, i * tile_size) for j in range(self.cols)] for i in range(self.rows)]
