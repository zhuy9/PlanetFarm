from django.db import models
import enum
import random

# Create your models here.


class AnimalType(enum.Enum):
    wolf = "wolf"
    sheep = "sheep"
    rabbit = "rabbit"
    eagle = "eagle"
    snake = "Snake"


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

    def simple_name(self):
        return self.type[0]

    def random_move(self, farm):
        new_x = self.x
        new_y = self.y
        dir = 1
        if random.randint(0, 1) == 0:
            dir *= -1
        if random.randint(0, 1) == 0:
            new_x += dir * self.move_speed
        else:
            new_y += dir * self.move_speed

        if farm.valid_pos(new_x, new_y) and not farm.is_occupied(new_x, new_y):
            self.x = new_x
            self.y = new_y

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

    def valid_pos(self, x, y):
        return 0 <= x and 0 <= y and x < self.rows and y < self.cols and self.tiles[x][y].type != TileType.WALL

    def is_occupied(self, x, y):
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
            ani.random_move(self)

    def random_position(self, animal):
        new_x = random.randint(0, self.rows - 1)
        new_y = random.randint(0, self.cols - 1)

        while self.is_occupied(new_x, new_y):
            new_x = random.randint(0, self.rows - 1)
            new_y = random.randint(0, self.cols - 1)

        animal.x = new_x
        animal.y = new_y

    def add_animal(self, animal, random=False):
        if random:
            self.random_position(animal)
        self.animals.append(animal)

    def add_grass_randomly(self):
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)
        self.tiles[row][col].type = TileType.GRASS

    def add_fence_randomly(self):
        return 0
