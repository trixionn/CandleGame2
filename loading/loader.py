import json

import loading.sprite_loader as sprite_loader
from loading.loader_functions import *


class Loader:
	DEFAULT_CONFIG_PATH = 'loading/asset_config.json'  # relative
	DEFAULT_LEVELS_PATH = 'assets/levels'

	def __init__(self, initial_screen_size: tuple[int, int], config_path=None):
		self.W, self.H = initial_screen_size
		self.CONFIG_PATH = Loader.DEFAULT_CONFIG_PATH if config_path is None else config_path

		self.json_data = dict()

		self.scenes = dict()
		self.player = dict()
		self.levels = dict()

	def load_config(self):
		try:
			with open(self.CONFIG_PATH, 'rt', encoding='utf-8') as f:
				self.json_data = json.load(f)
		except FileNotFoundError:
			raise FileNotFoundError(
				f'Unable to load assets. Config file {self.CONFIG_PATH} was not found')
		except json.JSONDecodeError as e:
			raise ValueError(
				f'Unable to load assets. Config file {self.CONFIG_PATH} is corrupted.\nDetails: {e}')

	def load_all(self):
		if not self.json_data:
			self.load_config()

		self.load_scenes()
		self.load_player(self.json_data['player']['lvl1'])
		self.load_levels()

	def load_scenes(self):
		for scene_name, scene_json in self.json_data['scenes'].items():
			self.scenes[scene_name] = dict()
			self.scenes[scene_name].update(self.load_scene(scene_json))

	def load_levels(self):
		for level_name, level_json in self.json_data['levels'].items():
			self.levels[level_name] = dict()
			self.levels[level_name].update(self.load_level(level_name, level_json))

	def load_scene(self, scene_json: dict):
		assets = dict()
		sheets = dict()
		loads_later = dict()

		# loading all absolute files, that don't have relations
		for asset_name, asset_json in scene_json.items():
			match asset_json['type']:
				case 'image':
					# this is original asset
					if asset_json['original']:
						asset = load_image(asset_json['path'])
						asset = self.scale_image(asset, asset_json['scale_factor'])
						assets[asset_name] = asset
					# this is realtive asset
					else:
						loads_later[asset_name] = asset_json
				case 'sheet':
					sheets[asset_name] = load_image(asset_json['path'])
				case 'font':
					asset = load_font(asset_json['path'], asset_json['size'])
					assets[asset_name] = asset

		# loading all relations
		for asset_name, asset_json in loads_later.items():
			sheet = sheets[asset_json['origin']]
			asset = load_image_relative(sheet, asset_json['frames'])
			asset = list(map(lambda a: self.scale_image(a, asset_json['scale_factor']), asset))
			assets[asset_name] = asset

		return assets

	def load_player(self, anims_json: dict):
		for anim_name, anim_json in anims_json.items():
			sheet = load_image(anim_json['path'])
			anim = sprite_loader.process_sheet(
				sheet,
				anim_json['rows'], anim_json['columns'],
				anim_json['names'],
				anim_json['amount'],
				anim_json['scale_factor']
			)
			self.player[anim_name] = anim

			# TODO: Move hitbox information into its own dedicated place.
			hitbox = list(map(lambda _: _ * anim_json['scale_factor'], anim_json['hitbox']))
			self.player[anim_name]['hitbox'] = hitbox

	def load_level(self, level_name: str, level_json) -> dict:
		sectors = dict()

		for sector_str, sector_json in level_json.items():
			x, y = map(int, sector_str.split(' '))
			if x in sectors:
				sectors[x][y] = dict()
			else:
				sectors[x] = {y: dict()}
			sectors[x][y]['_bounds'] = sector_json['bounds']

			for asset_name, asset_json in sector_json['assets'].items():
				path = f'{self.DEFAULT_LEVELS_PATH}/{level_name}/{asset_json['name']}'
				match asset_json['type']:
					case 'image':
						asset = load_image(path)
						asset = self.scale_image(asset, asset_json['scale_factor'])
						sectors[x][y][asset_name] = asset
		return sectors

	def scale_image(self, surf: pg.Surface, factor):
		"""scale factor 0 is for images of screen size. (e.g., Background)"""

		if factor == 0:
			return pg.transform.scale(surf, (self.W, self.H))
		return pg.transform.scale_by(surf, factor)
