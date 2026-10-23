import pygame as pg


class Renderer:
	resolution = (1280, 720)
	title = 'Candle Game 2'

	def __init__(self):
		self._screen = pg.display.set_mode(Renderer.resolution)
		pg.display.set_caption(Renderer.title)

	@staticmethod
	def render():
		pg.display.flip()

	def get_screen_size(self):
		return self._screen.get_size()

	def blit(self, surf: pg.Surface, rect: pg.Rect | tuple = (0, 0)):
		self._screen.blit(surf, rect)

	def blit_rect(self, color, rect: pg.Rect, **kwargs):
		pg.draw.rect(self._screen, color, rect, **kwargs)

	def blits(self, objects: list):
		for obj in objects:
			self.blit(obj[0], obj[1])

	def fill_bg(self, color):
		self._screen.fill(color)
