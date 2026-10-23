import pygame as pg

import debug
from engine import GameEngine


class App:
	def __init__(self):
		pg.init()
		self.game_engine = GameEngine()

	def run(self):
		self.game_engine.run()


if __name__ == '__main__':
	debug.configure(True)
	app = App()
	app.run()
