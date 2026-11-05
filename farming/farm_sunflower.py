# Sunflower: plant the whole farm, then harvest from the most petals to the fewest.
# Harvesting the largest sunflower pays 8x, so tiles are replanted only after a full round.
# The bonus needs at least 10 sunflowers on the farm, so the last 9 stay standing.
# Each drone reports its tiles by petal count, so every round visits only matching tiles.
# Stops at the leaderboard goal: 100000 power with drones, 10000 with a single drone.
clear()
n = get_world_size()
goal = 10000
if max_drones() > 1:
	goal = 100000
d = max_drones()
if d > n:
	d = n

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

def plant_lane(x0, x1):
	found = {}
	up = True
	for x in range(x0, x1):
		for k in range(n):
			y = k
			if not up:
				y = n - 1 - k
			goto(x, y)
			if get_ground_type() != Grounds.Soil:
				till()
			if get_entity_type() != Entities.Sunflower:
				plant(Entities.Sunflower)
			petals = measure()
			if petals not in found:
				found[petals] = []
			found[petals].append((x, y))
		up = not up
	return found

def harvest_tiles(tiles):
	for p in tiles:
		goto(p[0], p[1])
		while not can_harvest():
			pass
		harvest()
	return True

def run_round(lanes, petals):
	drones = []
	own = []
	for i in range(len(lanes)):
		if petals in lanes[i]:
			if i == 0:
				own = lanes[i][petals]
			else:
				h = spawn_drone(harvest_tiles, lanes[i][petals])
				if h == None:
					harvest_tiles(lanes[i][petals])
				else:
					drones.append(h)
	harvest_tiles(own)
	for h in drones:
		wait_for(h)

while num_items(Items.Power) < goal:
	drones = []
	for i in range(1, d):
		h = spawn_drone(plant_lane, i * n // d, (i + 1) * n // d)
		drones.append(h)
	lanes = [plant_lane(0, n // d)]
	for h in drones:
		lanes.append(wait_for(h))
	remaining = 0
	for lane in lanes:
		for petals in lane:
			remaining += len(lane[petals])
	for i in range(9):
		petals = 15 - i
		count = 0
		for lane in lanes:
			if petals in lane:
				count += len(lane[petals])
		keep = 9 - (remaining - count)
		for lane in lanes:
			while keep > 0 and petals in lane and len(lane[petals]) > 0:
				lane[petals].pop()
				keep -= 1
				count -= 1
		run_round(lanes, petals)
		remaining -= count
		if remaining <= 9:
			break
