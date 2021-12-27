import sys
from random import random
import time


DIRECTION_SYMBOLS = ">v<^"
SYMBOL_TO_DIRECTION = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}


def turn(symbol, count):
    i = DIRECTION_SYMBOLS.index(symbol)
    i += count
    i %= len(DIRECTION_SYMBOLS)
    return DIRECTION_SYMBOLS[i]


def print_map(roads, cars):
    for y, row in enumerate(roads):
        print("".join(cars.get((x, y, 0), " ."[c != "."]) for x, c in enumerate(row)))


def get_moves(roads, cars, symbol):
    width = len(roads[0])
    height = len(roads)

    dx, dy = SYMBOL_TO_DIRECTION[symbol]
    reversed_symbol = turn(symbol, 2)

    for position, car in cars.items():
        if car == symbol:
            x, y, z = position

            new_x = (x + dx) % width
            new_y = (y + dy) % height

            new_position = new_x, new_y, z

            if roads[new_y][new_x] not in (".", reversed_symbol) and new_position not in cars:
                new_road = roads[y][x]

                for i in range(4):
                    new_road = turn(new_road, 1)
                    neighbor_dx, neighbor_dy = SYMBOL_TO_DIRECTION[new_road]

                    neighbor_x = (x + neighbor_dx) % width
                    neighbor_y = (y + neighbor_dy) % height

                    if roads[neighbor_y][neighbor_x] == new_road:
                        break

                new_car = roads[new_y][new_x]
                yield position, new_position, new_car, new_road
            else:
                new_car = turn(symbol, 1)
                yield position, position, new_car, roads[y][x]


def main():
    roads = [[road for road in line.strip()] for line in  sys.stdin]

    for row in roads:
        if len(row) != len(roads[0]):
            raise Exception("row length mismatch")

    cars = {}

    for y, row in enumerate(roads):
        for x, c in enumerate(row):
            if c in DIRECTION_SYMBOLS and random() < 0.5:
                cars[x, y, 0] = c

    while True:
        for symbol in DIRECTION_SYMBOLS:
            for position, new_position, new_car, new_road in list(get_moves(roads, cars, symbol)):
                x, y, z = position
                roads[y][x] = new_road

                if new_position != position:
                    del cars[position]

                cars[new_position] = new_car

            sys.stdout.write("\x1b[2J\x1b[H")
            print_map(roads, cars)
            time.sleep(0.05)


if __name__ == "__main__":
    main()
