# Maze: one maze per drone, reused until the treasure has been moved 300 times.
# Each drone remembers the paths it has seen, so later trips take the shortest known route.
# Reusing also skips harvesting, replanting, and growing a new maze for every treasure.
# Stops at the leaderboard goal: 9863168 gold with drones, 616448 with a single drone.
clear()
n = get_world_size()
goal = 616448
if max_drones() > 1:
	goal = 9863168
d = max_drones()
grid = 1
while grid * grid < d:
	grid += 1
side = n // grid
level = 2 ** (num_unlocked(Unlocks.Mazes) - 1)
substance = side * level
value = side * side * level
moves = [(North, 0, 1, South), (East, 1, 0, West), (South, 0, -1, North), (West, -1, 0, East)]

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

def open_moves(known, x, y):
	if (x, y) not in known:
		found = []
		for m in moves:
			if can_move(m[0]):
				found.append(m)
		known[(x, y)] = found
	return known[(x, y)]

def walk_known(known, tx, ty):
	start = (get_pos_x(), get_pos_y())
	came = {start: None}
	queue = [start]
	i = 0
	while i < len(queue) and (tx, ty) not in came:
		p = queue[i]
		i += 1
		if p in known:
			for m in known[p]:
				q = (p[0] + m[1], p[1] + m[2])
				if q not in came:
					came[q] = (p, m[0])
					queue.append(q)
	if (tx, ty) not in came:
		return False
	path = []
	p = (tx, ty)
	while came[p] != None:
		path.append(came[p][1])
		p = came[p][0]
	for k in range(len(path)):
		move(path[len(path) - 1 - k])
	return True

def search(known, tx, ty):
	seen = {(get_pos_x(), get_pos_y()): True}
	back = []
	while get_pos_x() != tx or get_pos_y() != ty:
		x = get_pos_x()
		y = get_pos_y()
		best = None
		best_dist = 9999
		for m in open_moves(known, x, y):
			nx = x + m[1]
			ny = y + m[2]
			if (nx, ny) not in seen:
				dist = abs(tx - nx) + abs(ty - ny)
				if dist < best_dist:
					best = m
					best_dist = dist
		if best != None:
			move(best[0])
			seen[(x + best[1], y + best[2])] = True
			back.append(best[3])
		elif len(back) > 0:
			move(back.pop())
		else:
			return False
	return True

def run_maze(cx, cy):
	goto(cx, cy)
	harvest()
	plant(Entities.Bush)
	if not use_item(Items.Weird_Substance, substance):
		return False
	known = {}
	moved = 0
	while True:
		target = measure()
		if target == None:
			harvest()
			return False
		tx, ty = target
		if not walk_known(known, tx, ty) and not search(known, tx, ty):
			harvest()
			return False
		held = num_items(Items.Gold) + d * (moved + 1) * value
		if moved >= 300 or held >= goal or num_items(Items.Weird_Substance) < substance:
			harvest()
			return True
		use_item(Items.Weird_Substance, substance)
		moved += 1

def worker(cx, cy):
	while num_items(Items.Gold) < goal and num_items(Items.Weird_Substance) >= substance:
		run_maze(cx, cy)
	return True

drones = []
count = 0
for i in range(grid):
	for j in range(grid):
		if count > 0 and count < d:
			h = spawn_drone(worker, i * side + side // 2, j * side + side // 2)
			if h != None:
				drones.append(h)
		count += 1
worker(side // 2, side // 2)
for h in drones:
	wait_for(h)
