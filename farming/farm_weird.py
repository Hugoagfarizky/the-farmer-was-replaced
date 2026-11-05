# Weird Substance: fertilized carrots turn half of their yield into Weird Substance.
# Polyculture companions raise the yield, so each fertilizer gives more substance.
# Stops at the goal, or when the fertilizer runs out. Change goal to collect a different amount.
clear()
n = get_world_size()
goal = 2000000

def crop_at(x, y):
	return Entities.Carrot

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

def plant_crop(crop):
	if plant(crop) and num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)

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
	while num_items(Items.Weird_Substance) < goal and num_items(Items.Fertilizer) > 0:
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
					plant_crop(crop)
				else:
					continue
			elif can_harvest():
				harvest()
				if pos in partner:
					wanted.pop(partner[pos])
					partner.pop(pos)
				plant_crop(crop)
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
print("weird", num_items(Items.Weird_Substance), "fertilizer", num_items(Items.Fertilizer))
