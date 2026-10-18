import pygame as pg

from controls.handler import Handler
from eventbus import EventBus


class EventHandler:
	def __init__(self, ebus: EventBus):
		self.ebus = ebus
		self.controls = Handler(ebus)

	def handle(self, events: list[pg.event.Event]):
		self.controls.update()
		for e in events:
			if e.type == pg.QUIT:
				self.ebus.emit('shutdown')
			elif e.type in (pg.KEYUP, pg.KEYDOWN, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION, pg.MOUSEWHEEL):
				self.controls.handle(e)
