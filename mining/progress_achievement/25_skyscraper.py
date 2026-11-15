# Achievement: Skyscraper (place a block to reach the height of +150 z).
# One drone stacks a single pillar in the middle of the farm, until you stop it.
# Placed blocks may cave in when the columns next to them are much lower, and each block type has
# its own stability. So the drone first places one block of each kind it can place, reads their
# stability, and builds the pillar out of the most stable kind.
# Every block's result goes to output.txt, so if the pillar stops growing, the log shows where and why.
clear()
n = get_world_size()
for i in range(n // 2):
	move(East)
	move(North)

kinds = [Grounds.Block_Red, Grounds.Block_Green, Grounds.Block_Blue, Grounds.Rock, Grounds.Dirt]
best = Grounds.Block_Blue
best_s = -1
for g in kinds:
	if place(g):
		s = get_stability()
		quick_print("stability of", g, s)
		if s > best_s:
			best = g
			best_s = s
	else:
		quick_print("could not place", g)
quick_print("pillar made of", best, "stability", best_s)

last = get_pos_z()
while True:
	ok = place(best)
	z = get_pos_z()
	if not ok or z <= last:
		quick_print("placed", ok, "but z went from", last, "to", z, "ground", get_ground_type())
	elif z % 10 == 0:
		quick_print("z", z)
	last = z
