# Achievement: Long Distance Friendship (match a mushroom with a same-colored mushroom from a lower stratum).
# Measured with probe_mushroom on a 32x32 farm: stratum 1 starts at about z -629 and is a few blocks thick,
# stratum 2 starts at about z -704. Mushrooms survive digs next to them but cave in when a neighbor
# is more than 3 blocks deeper. Digging a mushroom gives nothing.
#
# A pushed block falls down any open column until it lands on the next block.
# Digging a shaft at B also clears the rock in the four tiles next to B (ring R), so each R becomes
# an open column down to stratum 2. The tile S two steps from B in the same direction still has its
# stratum 1 mushrooms, so a mushroom pushed from S toward R falls all the way onto R's stratum 2 top.
#
# One drone, until you stop it:
#   1. Dig a shaft at B through stratum 1 down to stratum 2, then one block more, so the R tiles
#      show their stratum 2 tops. Read their types.
#   2. For each direction, walk two tiles out to S and dig down to S's stratum 1. Push the top block
#      toward R when its type matches R's stratum 2 top, otherwise dig it away and try the next one.
#   3. Clear the farm and start over at a new B.
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

def ring_types():
	out = []
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Mushroom:
			out.append(measure(dr))
		else:
			out.append(None)
	return out

def attempt(bx, by):
	goto(bx, by)
	while get_ground_type() != Grounds.Mushroom:
		dig()
	z1 = get_pos_z()
	quick_print("B", bx, by, "stratum 1 at", z1)
	while get_ground_type() != Grounds.Mushroom or get_pos_z() > z1 - 10:
		dig()
	quick_print("stratum 2 at", get_pos_z(), "ring before", ring_types())
	dig()
	types = ring_types()
	quick_print("ring stratum 2 tops", types, "B now z", get_pos_z())
	for k in range(4):
		t = types[k]
		if t == None:
			continue
		move(dirs[k])
		quick_print(" dir", k, "R z", get_pos_z(), get_ground_type())
		move(dirs[k])
		quick_print(" dir", k, "S z", get_pos_z(), get_ground_type())
		while get_ground_type() != Grounds.Mushroom and get_pos_z() > z1 - 5:
			dig()
		quick_print(" S reached z", get_pos_z(), get_ground_type(), "R beside", get_ground_type(opposite(k)))
		while get_ground_type() == Grounds.Mushroom:
			s = measure()
			if s == t:
				ok = push(opposite(k))
				quick_print("  push type", s, "onto", t, "ok", ok)
				if ok:
					quick_print("  MATCH")
					return True
			dig()
		move(opposite(k))
		move(opposite(k))
	return False

bx = n // 2
by = n // 2
while True:
	clear()
	change_hat(Hats.Mining_Hat)
	attempt(bx, by)
	bx = (bx + 7) % n
	by = (by + 5) % n
