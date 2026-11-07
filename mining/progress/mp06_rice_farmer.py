# Achievement: Rice Farmer (farm a lot of rice).
# Every drone owns a band of rows and sweeps it, farming rice on the clay sheet under the dirt, until you stop it.
# Rice cycle on a tile: Clay -> plant -> Rice_Terrace (growing) -> Dry_Rice_Terrace (grown)
# -> harvest -> dig the dry block -> Clay below -> plant again.
# The clay sheet is only a few blocks thick. A tile is used up when there is dirt again under the clay,
# or when it is deeper than any clay seen and still has none. Once every tile is used up,
# the farm is cleared and the drones dig down to a fresh sheet.
n = get_world_size()
d = max_drones()
if d > n:
	d = n
h = n // d

# state per tile: 0 = no clay seen yet, 1 = clay seen, 2 = used up.
# low[0] is the deepest drone height at which this drone has stood on clay.
def visit(state, k, low):
	if state[k] == 2:
		return 1
	if can_harvest():
		harvest()
	g = get_ground_type()
	if g == Grounds.Dry_Rice_Terrace:
		dig()
		g = get_ground_type()
	if g == Grounds.Clay:
		state[k] = 1
		z = get_pos_z()
		if low[0] == None or z < low[0]:
			low[0] = z
		plant(Entities.Rice)
	elif g == Grounds.Rice_Terrace or g == Grounds.Dry_Rice_Terrace:
		state[k] = 1
	elif state[k] == 1:
		state[k] = 2
		return 1
	elif low[0] != None and get_pos_z() < low[0] - 1:
		state[k] = 2
		return 1
	else:
		dig()
	return 0

def worker(y0, rows):
	change_hat(Hats.Mining_Hat)
	for i in range(y0):
		move(North)
	state = []
	for i in range(rows * n):
		state.append(0)
	low = [None]
	while True:
		done = 0
		k = 0
		for r in range(rows):
			for i in range(n):
				done += visit(state, k, low)
				k += 1
				move(East)
			move(North)
		for r in range(rows):
			move(South)
		if done == rows * n:
			return True

while True:
	clear()
	drones = []
	for k in range(1, d):
		rows = h
		if k == d - 1:
			rows = n - h * (d - 1)
		dr = spawn_drone(worker, k * h, rows)
		if dr != None:
			drones.append(dr)
	if d == 1:
		worker(0, n)
	else:
		worker(0, h)
	for dr in drones:
		wait_for(dr)
