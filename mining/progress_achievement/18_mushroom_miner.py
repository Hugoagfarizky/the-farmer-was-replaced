# Achievement: Mushroom Miner (harvest 1,000 mushrooms).
# Mushroom blocks of the same type (measure() gives 0 to 5) are harvested when one lands on top of the other.
# push(direction) moves the mushroom block under the drone sideways. It fails if a block is in the way,
# and a block pushed over a lower column falls onto that column's top block.
# Digging next to mushroom blocks doesn't destroy them.
#
# Every drone starts in its own spot spread across the farm and works a "funnel" column there, until you stop it:
#   1. Dig down to the mushroom stratum, then dig one more block, so the funnel is lower than its neighbors.
#   2. Read the type on top of the funnel. If a neighboring column's top has the same type, step onto it,
#      push its top block into the funnel, and step back. The two blocks match and get harvested.
#      If no neighbor matches, or the push fails, dig the funnel's top block away to show the next type.
#   3. When the funnel has gone through the stratum, move three tiles over and start a new funnel.
#      After a row of funnels, it also moves three tiles north.
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

def opposite(dr):
	for i in range(4):
		if dirs[i] == dr:
			return dirs[(i + 2) % 4]

def match_side(b):
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Mushroom and measure(dr) == b:
			return dr
	return None

# low[0] is the deepest height at which this drone has stood on a mushroom block.
# Digging more than two blocks below it without finding mushrooms means this spot is used up.
def dig_to_stratum(low):
	while get_ground_type() != Grounds.Mushroom:
		if low[0] != None and get_pos_z() < low[0] - 2:
			return False
		dig()
	return True

def funnel(low):
	dig()
	while get_ground_type() == Grounds.Mushroom:
		z = get_pos_z()
		if low[0] == None or z < low[0]:
			low[0] = z
		b = measure()
		dr = match_side(b)
		pushed = False
		if dr != None:
			move(dr)
			pushed = push(opposite(dr))
			move(opposite(dr))
		if not pushed:
			dig()

def worker(x, y):
	change_hat(Hats.Mining_Hat)
	goto(x, y)
	low = [None]
	steps = 0
	while True:
		if dig_to_stratum(low):
			funnel(low)
		for i in range(3):
			move(East)
		steps += 1
		if steps >= n // 3:
			steps = 0
			for i in range(3):
				move(North)

count = 0
for i in range(grid):
	for j in range(grid):
		if count > 0 and count < d:
			spawn_drone(worker, i * space + space // 2, j * space + space // 2)
		count += 1
worker(space // 2, space // 2)
