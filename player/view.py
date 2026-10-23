import pygame as pg

import debug
from renderer import Renderer
from player.model import PlayerModel
from player.utils import Direction


class PlayerView:
	ANIM_SPEED = 5

	def __init__(self, model: PlayerModel, anims, renderer: Renderer):
		self.anims: dict[str, dict[str, list[pg.Surface]]] = anims
		self.index = 0
		self.model = model
		self.direction: Direction = PlayerModel.DEFAULT_DIRECTION
		self.current_anim = 'idle'
		self.renderer = renderer

	def update(self, dt):
		self.calc_direction()
		self.current_anim = 'walk' if self.model.speedx or self.model.speedy else 'idle'
		self.index = (self.index + PlayerView.ANIM_SPEED * dt) % len(self.anims[self.current_anim][self.direction])

	def get_frame(self):
		return self.anims[self.current_anim][self.direction][int(self.index)]

	def calc_direction(self):
		if self.model.speedx < 0:
			self.direction = Direction.LEFT
		elif self.model.speedx > 0:
			self.direction = Direction.RIGHT

		if self.model.speedy < 0:
			self.direction = Direction.UP
		elif self.model.speedy > 0:
			self.direction = Direction.DOWN

	def draw(self):
		self.renderer.blit(self.get_frame(), self.model.rect)

	def debug_draw(self):
		if not debug.flags.enabled:
			return

		if debug.flags.show_rects:
			self.renderer.blit_rect('yellow', self.model.rect, width=2)
		if debug.flags.show_hitboxes:
			self.renderer.blit_rect('red', self.model.hitbox, width=2)
