# Pumpkin: one giant pumpkin covering the whole farm, one lane of columns per drone.
# Each drone revisits only the tiles that are still growing or dead.
# Stops at the leaderboard goal: 200 million with drones, 10 million with a single drone.
clear()
n = get_world_size()
goal = 10000000
if max_drones() > 1:
	goal = 200000000
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

def tend(x0, x1):
	pending = []
	up = True
	for x in range(x0, x1):
		for k in range(n):
			if up:
				pending.append((x, k))
			else:
				pending.append((x, n - 1 - k))
		up = not up
	while len(pending) > 0:
		still = []
		for p in pending:
			goto(p[0], p[1])
			if get_entity_type() == Entities.Pumpkin:
				if not can_harvest():
					still.append(p)
			else:
				if get_ground_type() != Grounds.Soil:
					till()
				plant(Entities.Pumpkin)
				still.append(p)
		pending = still
	return True

while num_items(Items.Pumpkin) < goal:
	drones = []
	for i in range(1, d):
		h = spawn_drone(tend, i * n // d, (i + 1) * n // d)
		if h != None:
			drones.append(h)
	tend(0, n // d)
	for h in drones:
		wait_for(h)
	harvest()
