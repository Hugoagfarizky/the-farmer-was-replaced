# Achievement: Long Distance Friendship (match a mushroom with a same-colored mushroom from a lower stratum).
#
# What earlier runs showed:
#   - The strata sit at different depths after every clear (for example -490 and -634, or -74 and -260).
#   - Digging a mushroom gives nothing. Mushrooms survive digs next to them, but cave in when a
#     neighboring column is more than 3 blocks deeper (stability 3).
#   - A deep shaft makes the land around it cave in like a bowl, so a mushroom from the upper stratum
#     can't just wait next to a shaft and be pushed in. It caves in first.
#
# So this carries a mushroom down like an elevator, until you stop it:
#   1. Dig at B through the upper stratum. The four neighboring tiles keep their mushrooms.
#   2. Push one neighbor's top mushroom M into B. M lands on B's column, and the drone stands on it.
#   3. Dig the column E next to B one block at a time. Each dig removes the block next to it in B,
#      which is the rock under M, so M drops one level. E is never more than 1 deeper, so M doesn't cave in.
#   4. When M stops dropping, it is resting on the lower stratum. If the types match, both get harvested.
#      If not, dig E's top up to twice and push M into E when E's top has M's type.
#   5. Clear the farm and try again somewhere else.
# Every step is written to output.txt with quick_print, so a failed run shows what happened.
n = get_world_size()
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

def opposite(k):
	return dirs[(k + 2) % 4]

def top_type(dr):
	if get_ground_type(dr) == Grounds.Mushroom:
		return measure(dr)
	return get_ground_type(dr)

def ring():
	out = []
	for dr in dirs:
		out.append(top_type(dr))
	return out

def attempt(bx, by):
	goto(bx, by)
	while get_ground_type() != Grounds.Mushroom:
		dig()
	z1 = get_pos_z()
	quick_print("B", bx, by, "upper stratum at", z1, "ring", ring())
	while get_ground_type() == Grounds.Mushroom:
		dig()
	quick_print("B through the upper stratum, z", get_pos_z(), get_ground_type(), "ring", ring())

	# Step 2: push a neighbor's top mushroom into B.
	k = None
	for i in range(4):
		if k == None and get_ground_type(dirs[i]) == Grounds.Mushroom:
			k = i
	if k == None:
		quick_print("no mushroom next to B")
		return False
	m = measure(dirs[k])
	move(dirs[k])
	quick_print("on neighbor", k, "z", get_pos_z(), "type", m)
	ok = push(opposite(k))
	move(opposite(k))
	quick_print("push into B ok", ok, "B z", get_pos_z(), top_type(None))
	if not ok or get_ground_type() != Grounds.Mushroom:
		return False

	# Step 3: the elevator. E is a neighbor of B other than where M came from.
	e = (k + 1) % 4
	last = get_pos_z()
	still = 0
	gained = num_items(Items.Mushroom)
	while still < 2:
		move(dirs[e])
		dig()
		ez = get_pos_z()
		eg = get_ground_type()
		move(opposite(e))
		bz = get_pos_z()
		bg = get_ground_type()
		got = num_items(Items.Mushroom) - gained
		quick_print(" E z", ez, eg, "| B z", bz, bg, "mushrooms gained", got)
		if got > 0:
			quick_print("MATCH while dropping")
			return True
		if bg != Grounds.Mushroom:
			quick_print("M is gone")
			return False
		if ez < bz and bz == last:
			still += 1
		else:
			still = 0
		last = bz
		if bz < z1 - 600:
			quick_print("too deep")
			return False

	# Step 4: M rests on something special. Try E's top below it.
	quick_print("M stopped at z", get_pos_z(), "type", measure(), "E top", top_type(dirs[e]))
	for j in range(3):
		if top_type(dirs[e]) == m:
			ok = push(dirs[e])
			quick_print(" push M into E ok", ok, "mushrooms gained", num_items(Items.Mushroom) - gained)
			if ok:
				return True
		if j < 2:
			move(dirs[e])
			dig()
			move(opposite(e))
	quick_print("no match this time")
	return False

bx = n // 2
by = n // 2
while True:
	clear()
	change_hat(Hats.Mining_Hat)
	attempt(bx, by)
	bx = (bx + 7) % n
	by = (by + 5) % n
