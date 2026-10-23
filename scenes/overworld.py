from scenes.scene import Scene
from eventbus import EventBus
from player.entity import Player
from scenes.level_map import LevelMap
from renderer import Renderer


class Overworld(Scene):
	def __init__(self, renderer: Renderer, assets, ebus: EventBus, change_scene_action, **data):
		super().__init__(renderer, ebus, change_scene_action)
		self.name = 'overworld'
		self.assets = assets
		self.surfs, self.rects = self._load()

		self.level_map: LevelMap = data['level_map']

		self.player: Player = data['player']
		self.player.model.set_pos(center=self.CENTER)

	def _load(self):
		surfs = {
			'bg': self.assets['bg']
		}
		rects = {
			'bg': surfs['bg'].get_rect()
		}
		return surfs, rects

	def update(self, dt):
		self.interface.update()
		self.player.update(dt)

	def draw(self):
		self.renderer.fill_bg('lightblue')
		self.level_map.draw_frame()
		self.interface.draw()
		self.player.draw()
