# Achievement: Rice Farmer (farm a lot of rice).
# Same start as mp05_rice_terrace, then the rice is harvested and replanted over and over, until you stop it.
# Phase 1: every drone digs each tile of its band of rows down to the clay sheet.
# Phase 2: once every drone is done digging, every drone farms rice on its band:
#   Clay -> plant -> Rice_Terrace (growing) -> Dry_Rice_Terrace (grown)
#   -> harvest -> dig the dry block -> Clay below -> plant again.
# The clay sheet is only a few blocks thick. A tile is used up when there is no clay under the dry block.
# Once every tile of every band is used up, the farm is cleared and both phases start again on a fresh sheet.
n = get_world_size()
d = max_drones()
if d > n:
	d = n
h = n // d

def band_rows(k):
	if d == 1:
		return n
	if k == d - 1:
		return n - h * (d - 1)
	return h

def dig_band(y0, rows):
	change_hat(Hats.Mining_Hat)
	for i in range(y0):
		move(North)
	for r in range(rows):
		for i in range(n):
			while get_ground_type() != Grounds.Clay:
				dig()
			move(East)
		move(North)
	return True

def farm_band(y0, rows):
	change_hat(Hats.Mining_Hat)
	for i in range(y0):
		move(North)
	used = []
	for i in range(rows * n):
		used.append(False)
	left = rows * n
	while left > 0:
		k = 0
		for r in range(rows):
			for i in range(n):
				if not used[k]:
					if can_harvest():
						harvest()
					g = get_ground_type()
					if g == Grounds.Dry_Rice_Terrace:
						dig()
						g = get_ground_type()
					if g == Grounds.Clay:
						plant(Entities.Rice)
					elif g != Grounds.Rice_Terrace:
						used[k] = True
						left -= 1
				k += 1
				move(East)
			move(North)
		for r in range(rows):
			move(South)
	return True

def run(task):
	drones = []
	for k in range(1, d):
		dr = spawn_drone(task, k * h, band_rows(k))
		if dr != None:
			drones.append(dr)
	return drones

while True:
	clear()
	drones = run(dig_band)
	dig_band(0, band_rows(0))
	for dr in drones:
		wait_for(dr)

	# The main drone is at the top of its band after digging, so it walks back to the first row.
	for i in range(band_rows(0)):
		move(South)
	drones = run(farm_band)
	farm_band(0, band_rows(0))
	for dr in drones:
		wait_for(dr)
