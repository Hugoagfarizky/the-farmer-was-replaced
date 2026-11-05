# Wood: trees on a checkerboard with bushes between them, plus polyculture companions.
# Trees grow slower next to other trees, so they never touch along an edge.
# Stops at the leaderboard goal: 10 billion with drones, 500 million with a single drone.
clear()
n = get_world_size()
goal = 500000000
if max_drones() > 1:
	goal = 10000000000

def crop_at(x, y):
	if (x + y) % 2 == 0:
		return Entities.Tree
	return Entities.Bush

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

def set_ground(crop):
	soil = get_ground_type() == Grounds.Soil
	if (crop == Entities.Carrot and not soil) or (crop == Entities.Grass and soil):
		till()

def make_route(x0, x1, y0, y1):
	route = []
	up = True
	for x in range(x0, x1):
		if up:
			for y in range(y0, y1):
				route.append((x, y))
		else:
			for k in range(y1 - y0):
				route.append((x, y1 - 1 - k))
		up = not up
	return route

def worker(x0, x1, y0, y1):
	wanted = {}
	partner = {}
	route = make_route(x0, x1, y0, y1)
	while num_items(Items.Wood) < goal:
		for pos in route:
			goto(pos[0], pos[1])
			crop = crop_at(pos[0], pos[1])
			e = get_entity_type()
			if pos in wanted:
				t = wanted[pos]
				if e != t and (e == None or e == Entities.Grass or can_harvest()):
					if pos in partner:
						wanted.pop(partner[pos])
						partner.pop(pos)
					harvest()
					set_ground(t)
					plant(t)
				continue
			if e != crop:
				if e == None or can_harvest():
					harvest()
					set_ground(crop)
					plant(crop)
				else:
					continue
			elif can_harvest():
				harvest()
				if pos in partner:
					wanted.pop(partner[pos])
					partner.pop(pos)
				if crop != Entities.Grass:
					plant(crop)
			if pos not in partner:
				c = get_companion()
				if c != None:
					t, target = c
					tx, ty = target
					if tx >= x0 and tx < x1 and ty >= y0 and ty < y1 and target not in wanted:
						wanted[target] = t
						partner[pos] = target
	return True

d = max_drones()
rows = 1
while (rows + 1) * (rows + 1) <= d:
	rows += 1
while d % rows != 0:
	rows -= 1
cols = d // rows

drones = []
for i in range(cols):
	for j in range(rows):
		if i > 0 or j > 0:
			h = spawn_drone(worker, i * n // cols, (i + 1) * n // cols, j * n // rows, (j + 1) * n // rows)
			if h != None:
				drones.append(h)
worker(0, n // cols, 0, n // rows)
for h in drones:
	wait_for(h)
