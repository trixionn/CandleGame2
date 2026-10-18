from eventbus import EventBus
from interface import Interface
from renderer import Renderer


class Scene:
	def __init__(self, renderer: Renderer, ebus: EventBus, change_scene_action):
		self.name = 'DefaultScene'
		self.renderer = renderer
		self.W, self.H = self.renderer.get_screen_size()
		self.CENTER = self.W // 2, self.H // 2
		self.ebus = ebus
		self.interface = Interface(renderer)
		self.change_scene_action = change_scene_action

	def update(self, dt):
		self.interface.update()

	def draw(self):
		self.interface.draw()

	def on_load(self):
		pass

	def on_exit(self):
		pass
