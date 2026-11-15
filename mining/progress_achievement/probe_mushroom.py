# Probe, not an achievement: measures the mushroom strata so 20_matchmaker and 21_long_distance
# can be written for the real layout. It writes everything to output.txt with quick_print.
# One drone digs down through two mushroom strata at the middle of the farm, then stops.
clear()
change_hat(Hats.Mining_Hat)
n = get_world_size()
for i in range(n // 2):
	move(East)
	move(North)
dirs = [North, East, South, West]
quick_print("world", n, "drones", max_drones())

def neighbors():
	out = []
	for dr in dirs:
		g = get_ground_type(dr)
		if g == Grounds.Mushroom:
			out.append(measure(dr))
		else:
			out.append(g)
	return out

def stratum(k):
	while get_ground_type() != Grounds.Mushroom:
		dig()
	top = get_pos_z()
	quick_print("stratum", k, "top", top, "hardness", get_hardness(), "stability", get_stability())
	quick_print("  neighbors before", neighbors())
	col = []
	while get_ground_type() == Grounds.Mushroom:
		col.append(measure())
		before = num_items(Items.Mushroom)
		dig()
		quick_print("  dug type", col[len(col) - 1], "mushrooms gained", num_items(Items.Mushroom) - before, "now z", get_pos_z(), "neighbors", neighbors())
	quick_print("  column", col, "thickness", len(col), "bottom ground", get_ground_type(), "z", get_pos_z())

stratum(1)
stratum(2)
quick_print("done")
