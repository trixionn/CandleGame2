import pygame as pg

MOVE_RIGHT = 'move_right'
MOVE_LEFT = 'move_left'
MOVE_UP = 'move_up'
MOVE_DOWN = 'move_down'

DEFAULT_BINDS = {
	MOVE_RIGHT: (pg.K_d, pg.K_RIGHT),
	MOVE_LEFT: (pg.K_a, pg.K_LEFT),
	MOVE_UP: (pg.K_w, pg.K_UP),
	MOVE_DOWN: (pg.K_s, pg.K_DOWN),
}

CATEGORIES: dict[str, tuple[str, ...]] = {
	'movement': (MOVE_RIGHT, MOVE_LEFT, MOVE_UP, MOVE_DOWN)
}
