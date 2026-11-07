# Achievement: Coal Miner (mine a lot of coal).
# Every drone owns a band of rows and sweeps it tile by tile, one layer at a time, until you stop it.
# Coal only pays when the drone digs straight into it, and digging removes the four neighboring
# blocks at the same depth. So on each tile the drone:
#   - mines the tile if it is standing on coal,
#   - skips the tile if a neighbor is coal, so digging dirt here doesn't destroy that coal,
#   - digs the dirt otherwise, to go one layer deeper.
# The coal next to a skipped tile is mined when the sweep reaches it, and the tile is dug on a later pass.
clear()
change_hat(Hats.Mining_Hat)
n = get_world_size()
d = max_drones()
if d > n:
	d = n
h = n // d
dirs = [North, East, South, West]

def coal_next_to():
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Coal:
			return True
	return False

def visit():
	if get_ground_type() == Grounds.Coal:
		dig()
	elif not coal_next_to():
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
