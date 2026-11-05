# Cactus: plant the whole farm, sort rows and then columns in parallel, harvest once.
# The harvest pays the square of the harvested tiles, so a full farm matters most.
# Stops at the leaderboard goal: 33554432 with drones, 131072 with a single drone.
clear()
n = get_world_size()
goal = 131072
if max_drones() > 1:
	goal = 33554432
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

def sort_line(fwd, back):
	lo = 0
	hi = n - 1
	pos = 0
	while lo < hi:
		last = lo
		while pos < hi:
			if measure(fwd) < measure():
				swap(fwd)
				last = pos
			move(fwd)
			pos += 1
		hi = last
		last = hi
		while pos > lo:
			if measure(back) > measure():
				swap(back)
				last = pos
			move(back)
			pos -= 1
		lo = last
	while pos > 0:
		move(back)
		pos -= 1

def plant_rows(a, b):
	for y in range(a, b):
		goto(0, y)
		for x in range(n):
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Cactus)
			move(East)
	return True

def sort_rows(a, b):
	for y in range(a, b):
		goto(0, y)
		sort_line(East, West)
	return True

def sort_columns(a, b):
	for x in range(a, b):
		goto(x, 0)
		sort_line(North, South)
	return True

def parallel(task):
	drones = []
	for i in range(1, d):
		a = i * n // d
		b = (i + 1) * n // d
		h = spawn_drone(task, a, b)
		if h == None:
			task(a, b)
		else:
			drones.append(h)
	task(0, n // d)
	for h in drones:
		wait_for(h)

while num_items(Items.Cactus) < goal:
	parallel(plant_rows)
	parallel(sort_rows)
	parallel(sort_columns)
	goto(0, 0)
	harvest()
