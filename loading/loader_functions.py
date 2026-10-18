import pygame as pg


def load_font(path, size: int):
	try:
		font = pg.font.Font(path, size)
	except pg.error as e:
		raise ValueError(
			f'Unable to load assets. File {path}.\nDetails: {e}')
	return font


def load_image(path):
	try:
		image = pg.image.load(path)
	except pg.error as e:
		raise ValueError(
			f'Unable to load assets. File {path}.\nDetails: {e}')
	return image


def load_image_relative(sheet: pg.Surface, frames_preset: list) -> list[pg.Surface]:
	frames = []
	try:
		for preset in frames_preset:
			frames.append(sheet.subsurface(preset).copy())
	except pg.error as e:
		raise ValueError(
			f'Unable to load assets. Loading from sheet {sheet} failed.\nDetails: {e}')
	return frames



