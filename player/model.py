import pygame as pg
from math import inf

from eventbus import EventBus
from player.utils import Direction


class PlayerModel:
	MOVE_SPEED = 300
	DEFAULT_DIRECTION = Direction.LEFT

	def __init__(self, anims: dict[str, dict[str, list[pg.Surface]]], ebus: EventBus):
		self.ref_surf = anims['walk'][PlayerModel.DEFAULT_DIRECTION][0]
		self.rect: pg.Rect = self.ref_surf.get_rect()

		self.speedx = 0
		self.speedy = 0
		self.held = set()
		self.xbounds = tuple()
		self.ybounds = tuple()

		self.ebus = ebus
		ebus.subscribe(self.on_move, 'movement')

	def get_rect(self):
		return self.rect

	def get_pos(self):
		return self.rect.midbottom

	def set_pos(self, **pos):
		self.rect = self.ref_surf.get_rect(**pos)

	def set_bounds(self, xbounds, ybounds):
		self.xbounds = xbounds
		self.ybounds = ybounds

	def update(self, dt):
		self.move(dt)

	def move(self, dt):
		# print(self.rect.x, self.xbounds)
		newx = self.rect.left + self.speedx * dt
		newy = self.rect.top + self.speedy * dt

		if self.xbounds[0] < newx and newx + self.rect.width < self.xbounds[1]:
			self.rect.left = newx

		if self.ybounds[0] < newy and newy + self.rect.height < self.ybounds[1]:
			self.rect.top = newy

	def on_move(self, **data):
		if data['keydown']:
			self.held.add(data['action'])
		elif not data['keydown']:
			self.held.discard(data['action'])
		self._recompute_speed()

	def _recompute_speed(self):
		x = 0
		y = 0

		if 'move_right' in self.held: x += 1
		if 'move_left' in self.held: x -= 1
		if 'move_up' in self.held: y -= 1
		if 'move_down' in self.held: y += 1

		# diagonal movement ((0.7, 0.7) around unit vector)
		if x and y:
			x *= 0.7
			y *= 0.7

		self.speedx = PlayerModel.MOVE_SPEED * x
		self.speedy = PlayerModel.MOVE_SPEED * y
