import pygame as pg

from player.model import PlayerModel
from player.view import PlayerView

from eventbus import EventBus
from renderer import Renderer


class Player:
	def __init__(self, ebus: EventBus, anims, renderer: Renderer):
		self.anims = anims
		self.model = PlayerModel(self.anims, ebus)
		self.view = PlayerView(self.model, self.anims, renderer)
		self.renderer = renderer

	def update(self, dt):
		self.model.update(dt)
		self.view.update(dt)

	def draw(self):
		self.view.draw()
		self.view.debug_draw()
