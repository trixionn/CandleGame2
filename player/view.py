import pygame as pg

from player.model import PlayerModel
from player.utils import Direction


class PlayerView:
	ANIM_SPEED = 5

	def __init__(self, model: PlayerModel, anims):
		self.anims: dict[str, dict[str, list[pg.Surface]]] = anims
		self.index = 0
		self.model = model
		self.direction: Direction = PlayerModel.DEFAULT_DIRECTION
		self.current_anim = 'idle'

	def update(self, dt):
		self.calc_direction()
		self.current_anim = 'walk' if self.model.speedx or self.model.speedy else 'idle'
		self.index = (self.index + PlayerView.ANIM_SPEED * dt) % len(self.anims[self.current_anim][self.direction])

	def render(self, surf: pg.Surface, model: PlayerModel):
		surf.blit(self.get_frame(), model.rect)

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
