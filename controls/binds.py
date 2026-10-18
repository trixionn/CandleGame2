from controls.defaults import DEFAULT_BINDS, CATEGORIES


class KeyBinds:
	def __init__(self):
		self._map = self.load_from_file()
		self._action_from_key = {}
		self._category_from_action = {}
		self._rebuild_index()

	def __getitem__(self, action: str) -> tuple[int]:
		try:
			return self._map[action]
		except KeyError:
			raise KeyError(f'No {action} action or key was found in KeyBinds')

	def __setitem__(self, action: str, keys: tuple):
		if action in self._map:
			self._map[action] = keys
			self._rebuild_index()
		else:
			raise KeyError(f'No {action} action or key was found in KeyBinds')

	def _rebuild_index(self):
		self._category_from_action = {
			action: cat
			for cat, actions in CATEGORIES.items()
			for action in actions
		}
		self._action_from_key = {
			key: action
			for action, keys in self._map.items()
			for key in keys
		}

	def get_action(self, key: int):
		return self._action_from_key.get(key)

	def get_category(self, key: int):
		action = self.get_action(key)
		return self._category_from_action.get(action)

	@staticmethod
	def load_from_file():
		"""TODO: actual load from file"""

		return DEFAULT_BINDS
