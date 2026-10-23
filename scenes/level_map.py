from math import inf
import logging

from renderer import Renderer
from player.entity import Player

logger = logging.getLogger(__name__)


class LevelMap:
	INITIAL_LEVEL = 'level1'
	DEFAULT_BOUNDS = [[0, 1], [0, 1]]

	def __init__(self, level_assets: dict, renderer: Renderer, player: Player):
		self.renderer = renderer
		self.assets = level_assets

		self.current_level = LevelMap.INITIAL_LEVEL
		self.bounds = LevelMap.DEFAULT_BOUNDS
		self.sector = dict()
		self.sectorx = 0
		self.sectory = 0

		self.player_model = player.model
		screen_size = renderer.get_screen_size()
		self.screen_bounds = ((0, screen_size[0]), (0, screen_size[1]))

	def update(self):
		bound = self.player_out_of_bounds()
		if bound:
			self.change_sector(bound)

	def player_out_of_bounds(self) -> str | None:
		"""checks if the player is out of current sector's bounds.
		Returns crossed bound, else None."""

		pos = self.player_model.get_pos()
		if pos[0] < self.screen_bounds[0][0]:
			return 'left'

		if pos[0] > self.screen_bounds[0][1]:
			return 'right'

		if pos[1] < self.screen_bounds[1][0]:
			return 'top'

		if pos[1] > self.screen_bounds[1][1]:
			return 'bottom'

		return None

	def draw_frame(self):
		self.renderer.blit(self.sector['bg'])

	def set_level(self, level_name):
		if level_name not in self.assets:
			raise ValueError(f'Cant set level to "{level_name}". This level is not loaded or doesnt exist')

		self.current_level = level_name
		self.sector = self.assets[level_name][0][0]
		self.bounds = self.get_absolute_bounds(self.sector['_bounds'])
		self.player_model.set_bounds(*self.bounds)

	def get_absolute_bounds(self, relative_bounds):
		"""bounds default to [0, 1] initially,
		this function returns absolute values for the current size of the screen."""

		xbounds = relative_bounds[0]
		ybounds = relative_bounds[1]

		xbounds_min = -inf if xbounds[0] is None else xbounds[0]
		xbounds_max = inf if xbounds[1] is None else xbounds[1]
		ybounds_min = -inf if ybounds[0] is None else ybounds[0]
		ybounds_max = inf if ybounds[1] is None else ybounds[1]

		xbounds_min *= self.screen_bounds[0][1] if xbounds_min != -inf else 1
		xbounds_max *= self.screen_bounds[0][1] if xbounds_max != inf else 1
		ybounds_min *= self.screen_bounds[1][1] if ybounds_min != -inf else 1
		ybounds_max *= self.screen_bounds[1][1] if ybounds_max != inf else 1

		return (xbounds_min, xbounds_max), (ybounds_min, ybounds_max)

	def change_sector(self, direction):
		"""moves player accordingly to opposite bound of a sector, also sets variables."""

		logger.debug(f'Player moves in {direction}')
		match direction:
			case 'left':
				self.sectorx -= 1
				self.player_model.set_pos(right=self.screen_bounds[0][1])
			case 'right':
				self.sectorx += 1
				self.player_model.set_pos(left=self.screen_bounds[0][0])
			case 'top':
				self.sectory -= 1
				self.player_model.set_pos(bottom=self.screen_bounds[1][1])
			case 'bottom':
				self.sectory += 1
				self.player_model.set_pos(top=self.screen_bounds[1][0])

		self.sector = self.assets[self.current_level][self.sectorx][self.sectory]
		self.bounds = self.get_absolute_bounds(self.sector['_bounds'])
		self.player_model.set_bounds(*self.bounds)

		logger.debug(f'Player new sector {self.sector}, bounds {self.bounds}')


	def get_current_bounds(self):
		return (
			(self.screen_bounds[0][0] * self.bounds[0][0],
			self.screen_bounds[0][1] * self.bounds[0][1]),
			(self.screen_bounds[1][0] * self.bounds[1][0],
			self.screen_bounds[1][1] * self.bounds[1][1])
		)
