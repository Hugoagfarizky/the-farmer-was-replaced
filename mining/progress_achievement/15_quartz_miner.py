# Achievement: Quartz Miner (mine a lot of quartz).
# Same search as 14_quartz, run by every drone from its own spot spread across the farm, until you stop it.
# Quartz grows in vertical needles in the lower part of Grounds.Rock and the hard dirt below it.
# prospect_quartz() costs 1 iron and returns the 3D distance to the closest quartz block (None if none is near).
# Each drone digs down to the rock, then:
#   - standing on quartz or iron: dig it. The iron refills the stock that prospecting uses up.
#   - quartz in a neighboring tile: step onto it.
#   - otherwise: step one tile in the current heading and prospect again. If the distance went down,
#     stay there, otherwise step back and turn. Then dig one block.
# Digging removes the four neighboring blocks, so the neighbors are always as deep as the drone
# and it can step sideways without climbing back up. Each dig pulls the next ring down too.
# When iron runs out, prospect_quartz() returns None and the drones just dig down, so run 10_iron_miner first.
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

def quartz_next_to():
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Quartz:
			return dr
	return None

def worker(x, y):
	change_hat(Hats.Mining_Hat)
	goto(x, y)
	while get_ground_type() != Grounds.Rock:
		dig()
	heading = 0
	while True:
		g = get_ground_type()
		if g == Grounds.Quartz or g == Grounds.Iron:
			dig()
			continue
		q = quartz_next_to()
		if q != None:
			move(q)
			continue
		dist = prospect_quartz()
		if dist == None:
			for i in range(5):
				dig()
			continue
		for t in range(4):
			move(dirs[heading])
			d2 = prospect_quartz()
			if d2 != None and d2 < dist:
				break
			move(dirs[(heading + 2) % 4])
			heading = (heading + 1) % 4
		dig()

count = 0
for i in range(grid):
	for j in range(grid):
		if count > 0 and count < d:
			spawn_drone(worker, i * space + space // 2, j * space + space // 2)
		count += 1
worker(space // 2, space // 2)
