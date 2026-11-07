# Achievement: Rice Terrace (farm rice on the clay sheet).
# Every drone owns a band of rows and sweeps it, so rice is planted on every tile of the farm, until you stop it.
# Rice cycle on a tile: Clay -> plant -> Rice_Terrace (growing) -> Dry_Rice_Terrace (grown)
# -> harvest -> dig the dry block -> Clay below -> plant again.
# A tile that is still dirt is dug one layer per pass until it reaches the clay.
clear()
n = get_world_size()
d = max_drones()
if d > n:
	d = n
h = n // d

def visit():
	if can_harvest():
		harvest()
	g = get_ground_type()
	if g == Grounds.Dry_Rice_Terrace:
		dig()
		g = get_ground_type()
	if g == Grounds.Clay:
		plant(Entities.Rice)
	elif g != Grounds.Rice_Terrace:
		dig()

def worker(y0, rows):
	change_hat(Hats.Mining_Hat)
	for i in range(y0):
		move(North)
	while True:
		for r in range(rows):
			for i in range(n):
				visit()
				move(East)
			move(North)
		for r in range(rows):
			move(South)

for k in range(1, d):
	rows = h
	if k == d - 1:
		rows = n - h * (d - 1)
	spawn_drone(worker, k * h, rows)
if d == 1:
	worker(0, n)
else:
	worker(0, h)
