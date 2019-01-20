import argparse
from random import randint
from time import sleep
from copy import deepcopy
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clearConsole():
    os.system('cls' if os.name=='nt' else 'clear')


class GOL:
    def __init__(self, fieldSize, delay = 0.5):
        self.fieldSize = fieldSize
        self.initField()
        self.cellsRepresentation = {
            0: ' ',
            1: '#',
            2: bcolors.OKGREEN + '@' + bcolors.ENDC,
            3: bcolors.OKBLUE + '^' + bcolors.ENDC
        }
        self.delay = delay
    
    def initField(self):
        self.field = [[randint(0, 3) for _ in range(self.fieldSize)] for __ in range(self.fieldSize)]

    def calculateNeighbors(self, x, y, cellType):
        counter = 0

        if self.field[(y - 1 + self.fieldSize) % self.fieldSize][(x - 1 + self.fieldSize) % self.fieldSize] == cellType:
            counter += 1
        if self.field[(y - 1 + self.fieldSize) % self.fieldSize][(x + self.fieldSize) % self.fieldSize] == cellType:
            counter += 1
        if self.field[(y - 1 + self.fieldSize) % self.fieldSize][(x + 1 + self.fieldSize) % self.fieldSize] == cellType:
            counter += 1
        if self.field[(y + self.fieldSize) % self.fieldSize][(x + 1 + self.fieldSize) % self.fieldSize] == cellType:
            counter += 1
        if self.field[(y + 1 + self.fieldSize) % self.fieldSize][(x + 1 + self.fieldSize) % self.fieldSize] == cellType:
            counter += 1
        if self.field[(y + 1 + self.fieldSize) % self.fieldSize][(x + self.fieldSize) % self.fieldSize] == cellType:
            counter += 1
        if self.field[(y + 1 + self.fieldSize) % self.fieldSize][(x - 1 + self.fieldSize) % self.fieldSize] == cellType:
            counter += 1
        if self.field[(y + self.fieldSize) % self.fieldSize][(x - 1 + self.fieldSize) % self.fieldSize] == cellType:
            counter += 1

        return counter

    def calculateNextGeneration(self):
        nextGeneration = deepcopy(self.field)

        for y in range(self.fieldSize):
            for x in range(self.fieldSize):
                if self.field[y][x] == 0:
                    if self.calculateNeighbors(x, y, 2) == 3: # check if empty cell has 3 fish neighbors 
                        nextGeneration[y][x] = 2
                    elif self.calculateNeighbors(x, y, 3) == 3: # check if empty cell has 3 shrimp neighbors 
                        nextGeneration[y][x] = 3
                elif self.field[y][x] == 2 or self.field[y][x] == 3:
                    neighborsCounter = self.calculateNeighbors(x, y, self.field[y][x])
                    if neighborsCounter > 3 or neighborsCounter < 2:
                        nextGeneration[y][x] = 0

        self.field = nextGeneration

    def startGame(self):
        while True:
            print(self)
            print('\nPress ctrl + c to stop program from executing')
            self.calculateNextGeneration()
            sleep(self.delay)
            clearConsole()

    def __repr__(self):
        return '\n'.join(
                    ' '.join(str(self.cellsRepresentation.get(cell, cell)) for cell in row) for row in self.field 
                )

parser = argparse.ArgumentParser(description='Game of Life extended edition')
parser.add_argument('--size', '-s', type=int, action='store', help='Field size (5 by default)', default=5)
parser.add_argument('--delay', '-d', type=float, action='store', help='Delay before each step (0.5s by default)', default=0.5)
args = parser.parse_args()

gol = GOL(
            5 if args.size < 5 or args.size > 50 else args.size,
            args.delay
    )
gol.startGame()