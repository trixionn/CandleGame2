import pygame as pg


def process_sheet(surf: pg.Surface, rows: int, cols: int,
					names: tuple[str, ...], amount: tuple[int, ...], scale_by=1) -> dict[str, list[pg.Surface]]:
	if len(names) != rows or len(amount) != rows:
		raise TypeError('Amount of names must be the same as rows in a sprite sheet')

	w, h = surf.get_size()
	xstep, ystep = w // cols, h // rows  # OMG GD REFERENCE
	anims = {}

	for row in range(rows):
		anim = []
		anim_name = names[row]
		for col in range(amount[row]):
			sprite = surf.subsurface((col * xstep, row * ystep, xstep, ystep)).copy()

			if scale_by != 1:
				sprite = pg.transform.scale_by(sprite, scale_by)

			anim.append(sprite)
		anims[anim_name] = anim

	return anims
