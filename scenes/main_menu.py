import pygame as pg

from scenes.scene import Scene
from interface import Button
from eventbus import EventBus


class MainMenu(Scene):
	def __init__(self, renderer, assets, ebus: EventBus, change_scene_action, **data):
		super().__init__(renderer, ebus, change_scene_action)
		self.name = 'main_menu'
		self.assets = assets

		self.surfs, self.rects = self._load()
		self.ebus.subscribe(self.on_play, 'button_play_clicked')

	def _load(self):
		surfs = {
			'title': self.assets['main_font'].render('Candle Game 2', True, 'green'),
			'bg': pg.transform.scale(self.assets['bg'], (self.W, self.H))
		}
		rects = {
			'title': surfs['title'].get_rect(midtop=(self.W * 0.5, self.H * 0.1))
		}

		objs = {
			'button_play': Button(
				self.assets['button_play'], self.ebus, 'button_play_clicked',
				midtop=(self.W * 0.5, self.H * 0.4)),
			'button_settings': Button(
				self.assets['button_settings'], self.ebus, 'button_settings_clicked',
				midtop=(self.W * 0.5, self.H * 0.55)),
			'button_quit': Button(
				self.assets['button_quit'], self.ebus, 'shutdown',
				midtop=(self.W * 0.5, self.H * 0.7))
		}
		self.interface.set(objs)

		return surfs, rects

	def update(self, dt):
		self.interface.update()

	def draw(self):
		self.renderer.blit(self.surfs['bg'], (0, 0))
		self.renderer.blit(self.surfs['title'], self.rects['title'])
		self.interface.draw()

	def on_play(self, **data):
		self.change_scene_action('overworld')
