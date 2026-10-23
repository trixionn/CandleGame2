import pygame as pg

import debug
from eventbus import EventBus
from controls.binds import KeyBinds


class Handler:
	def __init__(self, ebus: EventBus):
		self.ebus = ebus
		self.keybinds = KeyBinds()

		self.mousepos = pg.mouse.get_pos()
		self.mouserel = pg.mouse.get_rel()
		self.mousebuts = pg.mouse.get_pressed()
		self.keys = pg.key.get_pressed()

	def handle(self, e: pg.event.Event):
		match e.type:
			case pg.KEYDOWN:
				self.ebus.emit('keydown', key=e.key)
				self.emit_movement(e.key, True)
				self.check_debug(e.key)
			case pg.KEYUP:
				self.ebus.emit('keyup', key=e.key)
				self.emit_movement(e.key, False)
			case pg.MOUSEBUTTONDOWN:
				self.ebus.emit('mousedown', button=e.button, pos=e.pos)
			case pg.MOUSEBUTTONUP:
				self.ebus.emit('mouseup', button=e.button, pos=e.pos)
			case pg.MOUSEMOTION:
				self.ebus.emit('mousemove', pos=e.pos, rel=e.rel, buttons=e.buttons)

	def emit_movement(self, key: int, keydown: bool):
		if self.keybinds.get_category(key) == 'movement':
			self.ebus.emit('movement', action=self.keybinds.get_action(key), keydown=keydown)

	def update(self):
		self.mousepos = pg.mouse.get_pos()
		self.mouserel = pg.mouse.get_rel()
		self.mousebuts = pg.mouse.get_pressed()

		self.keys = pg.key.get_pressed()
		pass

	@staticmethod
	def check_debug(key):
		match key:
			case pg.K_F1:
				debug.flags.show_rects = not debug.flags.show_rects
			case pg.K_F2:
				debug.flags.show_hitboxes = not debug.flags.show_hitboxes
			case pg.K_F3:
				debug.flags.show_fps = not debug.flags.show_fps
