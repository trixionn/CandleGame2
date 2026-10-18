import pygame as pg

from scenes.main_menu import MainMenu
from scenes.overworld import Overworld

from loading.loader import Loader
from player.entity import Player
from scenes.level_map import LevelMap


class SceneManager:
	TRANSITION = 2
	SCENES = {
		'main_menu': MainMenu,
		'overworld': Overworld
	}
	PLAYER_REQUIRED_SCENES = (
		'overworld'
	)
	LEVEL_MAP_REQUIRED_SCENES = (
		'overworld'
	)
	INITIAL = 'main_menu'

	def __init__(self, ebus, loader: Loader, renderer):
		self.scene = SceneManager.SCENES[SceneManager.INITIAL](
			renderer, loader.scenes[SceneManager.INITIAL], ebus, self.request_scene)
		self.next = None

		self.loader = loader
		self.renderer = renderer
		self.transition = SceneManager.TRANSITION
		self.ebus = ebus

		self.player = Player(self.ebus, self.loader.player, self.renderer)
		self.level_map = LevelMap(loader.levels, self.renderer, self.player)
		self.level_map.set_level('level1')

	def request_scene(self, scene):
		if self.next:
			return

		additional_data = dict()
		if scene in SceneManager.SCENES:
			if scene in SceneManager.PLAYER_REQUIRED_SCENES:
				additional_data['player'] = self.player

			if scene in SceneManager.LEVEL_MAP_REQUIRED_SCENES:
				additional_data['level_map'] = self.level_map

			new_scene = SceneManager.SCENES[scene](
				self.renderer, self.loader.scenes[scene], self.ebus, self.request_scene, **additional_data)
			self.next = new_scene

	def _apply(self):
		self.scene = self.next
		self.next = None

	def update(self, dt):
		if self.next:
			self.transition -= dt
			if self.transition <= 0:
				self._apply()
				self.transition = SceneManager.TRANSITION
				return

		self.scene.update(dt)
		self.level_map.update()

	def draw(self):
		self.scene.draw()
