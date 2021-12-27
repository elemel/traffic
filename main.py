import sys
from random import random
import time


DIRECTION_SYMBOLS = ">v<^"
SYMBOL_TO_DIRECTION = {">": (1, 0), "v": (0, 1), "<": (-1, 0), "^": (0, -1)}


def print_map(terrain, cars):
	for y, row in enumerate(terrain):
		print("".join(cars.get((x, y), " ."[c != "."]) for x, c in enumerate(row)))


def get_moves(terrain, cars, car_type):
	width = len(terrain[0])
	height = len(terrain)

	dx, dy = SYMBOL_TO_DIRECTION[car_type]

	for position, car in cars.items():
		if car == car_type:
			x, y = position

			new_x = (x + dx) % width
			new_y = (y + dy) % height

			new_position = new_x, new_y

			if terrain[new_y][new_x] != "." and new_position not in cars:
				yield position, new_position, car_type
			else:
				new_car_type = DIRECTION_SYMBOLS[(DIRECTION_SYMBOLS.index(car_type) + 1) % len(DIRECTION_SYMBOLS)]
				yield position, position, new_car_type


def main():
	terrain = list(map(str.strip, sys.stdin))

	for row in terrain:
		if len(row) != len(terrain[0]):
			raise Exception("row length mismatch")

	cars = {}

	for y, row in enumerate(terrain):
		for x, c in enumerate(row):
			if c in DIRECTION_SYMBOLS and random() < 0.5:
				cars[x, y] = c

	while True:
		for car_type in DIRECTION_SYMBOLS:
			for position, new_position, new_car_type in list(get_moves(terrain, cars, car_type)):
				if new_position != position:
					del cars[position]
					cars[new_position] = new_car_type
				elif new_car_type != car_type:
					cars[new_position] = new_car_type

			sys.stdout.write("\x1b[2J\x1b[H")
			print_map(terrain, cars)
			time.sleep(0.05)


if __name__ == "__main__":
	main()
