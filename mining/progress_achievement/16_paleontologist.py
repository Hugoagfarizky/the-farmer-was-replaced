# Achievement: Pumpkin Paleontologist (mine 1,000 petrified pumpkins).
# Petrified pumpkins sit in 3x3x3 or 5x5x5 cubes in the hard dirt under the rock layer,
# at about the same depth as quartz. Digging next to them doesn't destroy them.
# Every drone digs its own column, spread across the farm, until you stop it:
#   - standing on a petrified pumpkin, iron, or quartz: dig it.
#   - petrified pumpkin in a neighboring tile: step onto it, so the drone works its way through the whole cube.
#   - otherwise: dig down.
clear()
n = get_world_size()
d = max_drones()
grid = 1
while grid * grid < d:
	grid += 1
space = n // grid
dirs = [North, East, South, West]

def goto(x, y):
	dx = (x - get_pos_x()) % n
	if dx > n // 2:
		for i in range(n - dx):
			move(West)
	else:
		for i in range(dx):
			move(East)
	dy = (y - get_pos_y()) % n
	if dy > n // 2:
		for i in range(n - dy):
			move(South)
	else:
		for i in range(dy):
			move(North)

def pumpkin_next_to():
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Petrified_Pumpkin:
			return dr
	return None

def worker(x, y):
	change_hat(Hats.Mining_Hat)
	goto(x, y)
	while True:
		g = get_ground_type()
		if g == Grounds.Petrified_Pumpkin or g == Grounds.Iron or g == Grounds.Quartz:
			dig()
		else:
			dr = pumpkin_next_to()
			if dr != None:
				move(dr)
			else:
				dig()

count = 0
for i in range(grid):
	for j in range(grid):
		if count > 0 and count < d:
			spawn_drone(worker, i * space + space // 2, j * space + space // 2)
		count += 1
worker(space // 2, space // 2)
