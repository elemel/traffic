import sys
from random import random
import time


DIRECTIONS = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}


def print_map(terrain, cars):
	width = len(terrain[0])
	height = len(terrain)

	for y in range(height):
		print("".join(cars.get((x, y), ".") for x in range(width)))


def get_moves(terrain, cars, car_type):
	width = len(terrain[0])
	height = len(terrain)

	dx, dy = DIRECTIONS[car_type]

	for position, car in cars.items():
		if car == car_type:
			x, y = position

			new_x = (x + dx) % width
			new_y = (y + dy) % height

			new_position = new_x, new_y

			if new_position not in cars:
				yield position, new_position


def main():
	terrain = list(map(str.strip, sys.stdin))
	cars = {}

	for y, row in enumerate(terrain):
		for x, c in enumerate(row):
			if c in ">v<^" and random() < 0.25:
				cars[x, y] = c

	while True:
		for car_type in ">v<^":
			for a, b in list(get_moves(terrain, cars, car_type)):
				cars[b] = cars.pop(a)

			sys.stdout.write("\x1b[2J\x1b[H")
			sys.stdout.flush()
			print_map(terrain, cars)
			sys.stdout.flush()
			time.sleep(0.025)


if __name__ == "__main__":
	main()
