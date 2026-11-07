# Achievement: Iron Miner (mine a lot of iron).
# Every drone starts in its own spot spread across the farm and follows prospect_iron() to the closest
# iron ore, until you stop it. Each call costs 1 coal, so a stock of coal from 7_coal_miner helps.
# prospect_iron() returns None when the iron is straight below the drone, so then the drone digs down
# toward it and mines it. Iron veins also run downward, so the next ore is often right below.
# Coal and iron a drone lands on are mined on the way. Iron in a neighboring tile is reached without
# prospecting, and without coal the drone digs down and only checks its neighbors.
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
		g = get_ground_type()
		if g == Grounds.Iron or g == Grounds.Coal:
			dig()
		else:
			dr = iron_next_to()
			if dr == None and num_items(Items.Coal) > 0:
				dr = prospect_iron()
			if dr == None:
				dig()
			else:
				move(dr)

count = 0
for i in range(grid):
	for j in range(grid):
		if count > 0 and count < d:
			spawn_drone(worker, i * space + space // 2, j * space + space // 2)
		count += 1
worker(space // 2, space // 2)
