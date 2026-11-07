# Achievement: Rice Terrace (plant rice over the entire farm surface).
# Rice has to stand on every tile at the same time, so nothing is harvested here.
# Phase 1: every drone digs each tile of its band of rows down to the clay sheet.
# Phase 2: once every drone is done digging, every drone plants rice on its band,
# then keeps sweeping and replants any tile that has lost its rice, until you stop it.
# Digging waits for the whole farm first, so no digging happens next to rice that is already planted.
clear()
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

def plant_band(y0, rows):
	change_hat(Hats.Mining_Hat)
	for i in range(y0):
		move(North)
	while True:
		for r in range(rows):
			for i in range(n):
				if get_ground_type() == Grounds.Clay:
					plant(Entities.Rice)
				move(East)
			move(North)
		for r in range(rows):
			move(South)

def run(task):
	drones = []
	for k in range(1, d):
		dr = spawn_drone(task, k * h, band_rows(k))
		if dr != None:
			drones.append(dr)
	return drones

drones = run(dig_band)
dig_band(0, band_rows(0))
for dr in drones:
	wait_for(dr)

# The main drone is at the top of its band after digging, so it walks back to the first row.
for i in range(band_rows(0)):
	move(South)
run(plant_band)
plant_band(0, band_rows(0))
