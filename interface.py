import pygame as pg

from eventbus import EventBus
from renderer import Renderer


class Interface:
	def __init__(self, renderer: Renderer):
		self.objects: dict[str, 'Object'] = dict()
		self.renderer = renderer

	def add(self, name: str, obj: 'Object'):
		self.objects.update({name: obj})

	def set(self, objs: dict[str, 'Object']):
		self.objects.update(objs)

	def update(self):
		for name, obj in self.objects.items():
			obj.update()

	def draw(self):
		for name, obj in self.objects.items():
			self.renderer.blit(*obj.get_drawn())


class Object:
	def __init__(self, surf: pg.Surface, rect: pg.Rect):
		self.surf: pg.Surface = surf
		self.rect: pg.Rect = rect

	def update(self):
		pass

	def subscribe(self):
		pass

	def on_mousedown(self, **data):
		pass

	def on_mouseup(self, **data):
		pass

	def on_mousemove(self, **data):
		pass

	def get_drawn(self):
		return self.surf, self.rect


class Text(Object):
	def __init__(self, font: pg.font.Font, text: str, aa, color, **pos):
		self.font = font
		self.text = text
		self.aa = aa
		self.color = color

		self.rect = font.render(text, aa, color)
		self.rect = self.surf.get_rect(**pos)
		super().__init__(self.surf, self.rect)

	def update_text(self, text):
		self.text = text
		self.surf = self.font.render(text, self.aa, self.color)
		self.rect = self.surf.get_rect()

	def update_color(self, color):
		self.color = color
		self.surf = self.font.render(self.text, self.aa, color)
		self.rect = self.surf.get_rect()


class Button(Object):
	def __init__(self, frames: list[pg.Surface], ebus: EventBus, action: str = None, **pos):
		self.frames = frames
		self.index = 0
		self.surf: pg.Surface = self.frames[self.index]
		self.rect: pg.Rect = self.surf.get_rect(**pos)

		self.hovered = False
		self.pressed = False

		self.action = action
		self.ebus = ebus
		self.subscribe()

		super().__init__(self.surf, self.rect)

	def subscribe(self):
		self.ebus.subscribe(self.on_mousemove, 'mousemove')
		self.ebus.subscribe(self.on_mousedown, 'mousedown')
		self.ebus.subscribe(self.on_mouseup, 'mouseup')

	def update(self):
		self.index = self.hovered * 2 + self.pressed
		self.surf = self.frames[self.index]

	def on_mousedown(self, **data):
		if self.hovered and data['button'] == 1:
			self.pressed = True
			self.ebus.emit(self.action)

	def on_mouseup(self, **data):
		self.pressed = False

	def on_mousemove(self, **data):
		if self.rect.collidepoint(data['pos']):
			self.hovered = True
		else:
			self.hovered = False
			self.pressed = False
