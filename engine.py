import pygame as pg

from loading.loader import Loader
from renderer import Renderer
from scenes.manager import SceneManager
from events import EventHandler
from eventbus import EventBus


class GameEngine:
	def __init__(self):
		self.renderer = Renderer()
		self.ebus = EventBus()
		self.handler = EventHandler(self.ebus)

		self.loader = Loader(self.renderer.get_screen_size())
		self.loader.load_all()

		self.manager = SceneManager(self.ebus, self.loader, self.renderer)

		self.clock = pg.time.Clock()
		self.fps = 60
		self.running = True

	def run(self):
		dt = 0
		self.ebus.subscribe(self.shutdown, 'shutdown')

		while self.running:
			self.handler.handle(pg.event.get())

			self.manager.update(dt)
			self.manager.draw()

			self.renderer.render()
			dt = self.clock.tick(self.fps) / 1000

		self.on_exit()

	def shutdown(self, **data):
		self.running = False

	def on_exit(self):
		# autosave maybe?
		pg.quit()
