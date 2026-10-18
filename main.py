import pygame as pg
from engine import GameEngine


class App:
	def __init__(self):
		pg.init()
		self.game_engine = GameEngine()

	def run(self):
		self.game_engine.run()


if __name__ == '__main__':
	app = App()
	app.run()
