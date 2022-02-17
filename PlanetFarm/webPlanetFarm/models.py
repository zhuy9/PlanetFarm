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

    def url(self):
        return "/static/image/" + self.type.value + ".png"


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
        return str(self.type)[0]

    def url(self):
        return "/static/image/" + str(self.type) + ".png"

    def random_move(self, farm, dict):
        new_x = self.x
        new_y = self.y
        dir = 1
        if random.randint(0, 1) == 0:
            dir *= -1
        if random.randint(0, 1) == 0:
            new_x += dir * self.move_speed
        else:
            new_y += dir * self.move_speed

        if farm.valid_pos(new_x, new_y):
            dict[(self.x, self.y)].remove(self)
            self.x = new_x
            self.y = new_y
            add_to_dict(dict, self.x, self.y, self)

    def toString(self):
        return "I am a {} at ({},{})".format(self.type, self.x, self.y)


def add_to_dict(dict, x, y, obj):
    if (x, y) in dict:
        dict[(x, y)].append(obj)
    else:
        dict[(x, y)] = [obj]


class PlanetFarm:
    def __init__(self, rows, cols, tile_size):
        self.rows = rows
        self.cols = cols
        self.animals = []
        self.tiles = [[Tile(j * tile_size, i * tile_size)
                       for j in range(self.cols)] for i in range(self.rows)]
        self.values = self.toArray()
        self.grasses = []
        self.dict = {}

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def valid_pos(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols and self.tiles[x][y].type != TileType.WALL

    def is_occupied(self, x, y, animal):
        position = (x, y)
        if position not in self.dict:
            return False
        objs = self.dict[position]
        add_to_dict(self.dict, x, y, animal)
        if 'grass' in objs:
            for animal in objs:
                if not isinstance(animal, str):
                    return not (str(animal.type) == 'sheep' or str(animal.type) == 'rabbit')
        dict = {
            'sheep': None,
            'eagle': None,
            'rabbit': None,
            'snake': None,
            'wolf': None
        }
        for animal in objs:
            for ani in dict:
                if str(animal.type) == ani:
                    dict[ani] = animal
        self.dict[position].remove(animal)
        return not ((dict['sheep'] and dict['wolf']) or (dict['eagle'] and dict['snake']) or (dict['eagle'] and dict['rabbit']) or (dict['snake'] and dict['rabbit']))

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

    def toArray(self):
        arr = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                contain_animal = False
                for ani in self.animals:
                    if ani.x == row and ani.y == col:
                        arr[row][col] = ani.url()
                        contain_animal = True
                if not contain_animal:
                    arr[row][col] = self.tiles[row][col].url()
        return arr

    def update(self):
        for ani in self.animals:
            ani.random_move(self, self.dict)
        self.values = self.toArray()
        for position in self.dict:
            objs = self.dict[position]
            if 'grass' in objs:
                for animal in objs:
                    if not isinstance(animal, str):
                        if str(animal.type) == 'sheep' or str(animal.type) == 'rabbit':
                            self.dict[position].remove('grass')
                            self.tiles[position[0]][position[1]].type = TileType.PLAIN
                continue
            dict = {
                'sheep': None,
                'eagle': None,
                'rabbit': None,
                'snake': None,
                'wolf': None
            }
            for animal in objs:
                for ani in dict:
                    if str(animal.type) == ani:
                        dict[ani] = animal

            if dict['sheep'] and dict['wolf']:
                self.dict[position].remove(dict['sheep'])
                self.animals.remove(dict['sheep'])
            elif dict['eagle'] and dict['snake']:
                self.dict[position].remove(dict['snake'])
                self.animals.remove(dict['snake'])
            elif dict['eagle'] and dict['rabbit']:
                self.dict[position].remove(dict['rabbit'])
                self.animals.remove(dict['rabbit'])
            elif dict['snake'] and dict['rabbit']:
                self.dict[position].remove(dict['rabbit'])
                self.animals.remove(dict['rabbit'])
        print(self.dict)

    def random_position(self, animal):
        new_x = random.randint(0, self.rows - 1)
        new_y = random.randint(0, self.cols - 1)

        while self.is_occupied(new_x, new_y, animal):
            new_x = random.randint(0, self.rows - 1)
            new_y = random.randint(0, self.cols - 1)

        animal.x = new_x
        animal.y = new_y

    def add_animal(self, animal, random=False, coordinate=(1, 1)):
        if random:
            self.random_position(animal)
        else:
            animal.x = coordinate[0] - 1
            animal.y = coordinate[1] - 1
        self.animals.append(animal)
        add_to_dict(self.dict, animal.x, animal.y, animal)

    def add_grass_randomly(self):
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)
        self.tiles[row][col].type = TileType.GRASS
        self.grasses.append((row, col))
        add_to_dict(self.dict, row, col, 'grass')

    def add_grass(self, coordinate=(1, 1)):
        self.tiles[coordinate[0] - 1][coordinate[1] - 1].type = TileType.GRASS
        self.grasses.append((coordinate[0] - 1, coordinate[1] - 1))
        add_to_dict(self.dict, coordinate[0] - 1, coordinate[1] - 1, 'grass')

    def add_fence_randomly(self):
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)
        self.tiles[row][col].type = TileType.WALL

    def add_fence(self, coordinate=(1, 1)):
        self.tiles[coordinate[0] - 1][coordinate[1] - 1].type = TileType.WALL

    def get_animals(self):
        print([str(animal.type) for animal in self.animals])
        return [str(animal.type) for animal in self.animals]

    def get_grasses(self):
        return self.grasses
