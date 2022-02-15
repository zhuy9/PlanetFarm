from django.db import models
import enum
import random

# Create your models here.


class AnimalType(enum.Enum):
    wolf = "wolf"
    sheep = "sheep"
    rabbit = "rabbit"
    eagle = "eagle"
    snake = "snake"


class TileType(enum.Enum):
    GRASS = "G"
    PLAIN = "_"
    WALL = "W"


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = TileType.PLAIN

    def simple_name(self):
        return self.type.value


class Animal:
    def __init__(self, type: AnimalType):
        self.type = type
        self.x = 0
        self.y = 0
        self.move_speed = 1

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def random_position(self, row_upper, col_upper):
        self.x = random.randint(0, row_upper - 1)
        self.y = random.randint(0, col_upper - 1)

    def simple_name(self):
        return self.type[0]

    def random_move(self):
        self.x += 1

    def toString(self):
        return "I am a {} at ({},{})".format(self.type, self.x, self.y)


class PlanetFarm:
    def __init__(self, rows, cols, tile_size):
        self.rows = rows
        self.cols = cols
        self.animals = []
        self.tiles = [[Tile(j * tile_size, i * tile_size)
                       for j in range(self.cols)] for i in range(self.rows)]

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def contains_animal(self, x, y):
        for ani in self.animals:
            if ani.x == x and ani.y == y:
                return True
        return False

    def toString(self):
        map = ''
        for row in range(self.rows):
            for col in range(self.cols):
                contain_animal = False
                for ani in self.animals:
                    if ani.x == row and ani.y == col:
                        map += ani.simple_name() + " "
                        contain_animal = True
                if not contain_animal:
                    map += self.tiles[row][col].simple_name() + " "
            map += '\n'
        return map

    def update(self):
        for ani in self.animals:
            ani.random_move()

    def add_animal(self, animal, random=False):
        if random:
            animal.random_position(self.get_rows(), self.get_cols())
        self.animals.append(animal)
