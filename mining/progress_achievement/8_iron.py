# Achievement: Iron (mine an iron block).
# Iron is found in Grounds.Rock, below the dirt and the clay sheet. Its veins are small and hard to find,
# so every drone digs its own column, spread across the farm, until you stop it.
# Iron is a special block: digging next to it doesn't destroy it. So when a drone sees iron in one of
# the four neighboring tiles, it moves over there and mines it.
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

def iron_next_to():
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Iron:
			return dr
	return None

def worker(x, y):
	change_hat(Hats.Mining_Hat)
	goto(x, y)
	while True:
		if get_ground_type() == Grounds.Iron:
			dig()
		else:
			dr = iron_next_to()
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
