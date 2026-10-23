import pygame as pg

from eventbus import EventBus
from player.utils import Direction


class PlayerModel:
	MOVE_SPEED = 300
	DEFAULT_DIRECTION = Direction.LEFT

	def __init__(self, anims: dict[str, dict[str, list[pg.Surface] | list[int]]], ebus: EventBus):
		self.ref_surf = anims['walk'][PlayerModel.DEFAULT_DIRECTION][0]
		self.rect: pg.Rect = self.ref_surf.get_rect()

		if anims['walk'].get('hitbox'):
			offsetx, offsety, width, height = anims['walk']['hitbox']
			self.hitbox = pg.Rect(
				self.rect.left + offsetx, self.rect.top + offsety,
				width, height)
			self.offsetx, self.offsety = offsetx, offsety
		else:
			self.hitbox = self.rect
			self.offsetx, self.offsety = 0, 0

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
		return self.hitbox.center

	def set_pos(self, **pos):
		for key, val in pos.items():
			setattr(self.hitbox, key, val)
		self._update_rect_pos()

	def _update_rect_pos(self):
		self.rect.topleft = self.hitbox.left - self.offsetx, self.hitbox.top - self.offsety

	def set_bounds(self, xbounds, ybounds):
		self.xbounds = xbounds
		self.ybounds = ybounds

	def update(self, dt):
		self.move(dt)
		self._update_rect_pos()

	def move(self, dt):
		newx = self.hitbox.left + self.speedx * dt
		newy = self.hitbox.top + self.speedy * dt

		if self.xbounds[0] < newx and newx + self.hitbox.width < self.xbounds[1]:
			self.hitbox.left = newx

		if self.ybounds[0] < newy and newy + self.hitbox.height < self.ybounds[1]:
			self.hitbox.top = newy

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
