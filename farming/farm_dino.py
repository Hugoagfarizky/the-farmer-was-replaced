# Dinosaur: fill the farm with one tail, because bones pay the tail length squared.
# The drone follows a loop through every tile so it cannot trap itself, and cuts corners
# toward the apple while the tail still leaves enough room.
# Stops at the leaderboard goal of 33488928 bones, which is one full 32x32 tail.
clear()
k = get_world_size()
total = k * k
goal = 33488928
want = total - 2
moves = [(North, 0, 1), (East, 1, 0), (South, 0, -1), (West, -1, 0)]

def make_order():
	result = {}
	for x in range(k):
		for y in range(k):
			if x == 0:
				result[(x, y)] = y
			elif y == 0:
				result[(x, y)] = total - x
			elif x % 2 == 1:
				result[(x, y)] = k + (x - 1) * (k - 1) + (k - 1 - y)
			else:
				result[(x, y)] = k + (x - 1) * (k - 1) + (y - 1)
	return result

order = make_order()

def step(a, body, grew):
	x = get_pos_x()
	y = get_pos_y()
	h = order[(x, y)]
	reach = (a - h) % total
	room = total
	if len(body) > 0:
		room = (body[0] - h) % total
	best = None
	best_d = 0
	for m in moves:
		nx = x + m[1]
		ny = y + m[2]
		if nx >= 0 and nx < k and ny >= 0 and ny < k:
			d = (order[(nx, ny)] - h) % total
			if d > best_d and d <= reach and (d == 1 or d < room - 30):
				best = m[0]
				best_d = d
	if best == None or not move(best):
		return False
	body.append(h)
	if not grew:
		body.pop(0)
	return True

def grow():
	eaten = 0
	body = []
	grew = False
	change_hat(Hats.Dinosaur_Hat)
	target = measure()
	while eaten < want and target != None:
		a = order[target]
		while get_pos_x() != target[0] or get_pos_y() != target[1]:
			if not step(a, body, grew):
				change_hat(Hats.Straw_Hat)
				return eaten
			grew = False
		eaten += 1
		grew = True
		target = measure()
	step((order[(get_pos_x(), get_pos_y())] + 1) % total, body, grew)
	change_hat(Hats.Straw_Hat)
	return eaten

while num_items(Items.Bone) < goal:
	grow()
