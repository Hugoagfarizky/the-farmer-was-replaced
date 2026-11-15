# Achievement: Long Distance Friendship (match a mushroom with a same-colored mushroom from a lower stratum).
#
# What earlier runs showed:
#   - The strata sit at different depths after every clear (for example -490 and -634, or -74 and -260).
#   - Digging a mushroom gives nothing. Mushrooms survive digs next to them, but cave in when a
#     neighboring column is more than 3 blocks deeper (stability 3).
#   - A deep shaft makes the land around it cave in like a bowl, so a mushroom from the upper stratum
#     can't just wait next to a shaft and be pushed in. It caves in first.
#
#   - Removing the blocks next to a column doesn't take away the block under a mushroom, so a mushroom
#     doesn't drop when the column beside it is dug.
#
# So this walks a mushroom down a staircase, until you stop it:
#   1. Dig at B through the upper stratum. The four neighboring tiles keep their mushrooms.
#   2. Push one neighbor's top mushroom M into B. M lands on B's column.
#   3. Take turns with B and its neighbor E: dig the column M isn't on until its top is 3 below M,
#      then push M across. M falls 2 levels, and its neighbor is never more than 3 deeper, so it doesn't cave in.
#   4. In the lower stratum, stop digging as soon as the other column's top has M's type and push M
#      onto it. They match and get harvested.
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

	# Step 3: the staircase. M moves back and forth between B and its neighbor E, dropping 2 levels each time.
	# Removing blocks next to a column doesn't take away the block under M (an earlier run showed that),
	# so M only goes down by being pushed onto a lower column.
	# Mushrooms above `low` may still belong to the upper stratum, so M must not land on its own type there.
	low = get_pos_z() - 10
	e = (k + 1) % 4
	toward = [dirs[e], opposite(e)]
	side = 0
	gained = num_items(Items.Mushroom)
	while True:
		ml = get_pos_z()
		if ml < z1 - 1500:
			quick_print("too deep")
			return False
		move(toward[side])
		# Dig the other column down until its top is 3 below M. In the lower stratum, stop early
		# when its top has M's type, so M lands on it and they match.
		found = False
		while get_pos_z() > ml - 3 and not found:
			if get_pos_z() < ml and get_pos_z() < low and get_ground_type() == Grounds.Mushroom and measure() == m:
				found = True
			else:
				dig()
		tz = get_pos_z()
		tg = top_type(None)
		move(toward[1 - side])
		ok = push(toward[side])
		got = num_items(Items.Mushroom) - gained
		quick_print(" M z", ml, "-> other top z", tz, tg, "found", found, "push ok", ok, "mushrooms gained", got)
		if got > 0:
			quick_print("MATCH")
			return True
		if not ok:
			quick_print("push failed")
			return False
		move(toward[side])
		if get_ground_type() != Grounds.Mushroom:
			quick_print("M is gone at z", get_pos_z())
			return False
		side = 1 - side

bx = n // 2
by = n // 2
while True:
	clear()
	change_hat(Hats.Mining_Hat)
	attempt(bx, by)
	bx = (bx + 7) % n
	by = (by + 5) % n
