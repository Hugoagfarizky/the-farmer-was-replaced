# Achievement: Skyscraper (place a block to reach the height of +150 z).
# One drone stacks blue blocks on the middle of the farm until you stop it.
# It writes the height and the stability of the top block to output.txt after every block, so if
# the tower caves in before +150, the log shows how high it got and why.
clear()
n = get_world_size()
for i in range(n // 2):
	move(East)
	move(North)
last = get_pos_z()
quick_print("start z", last)
while True:
	ok = place(Grounds.Block_Blue)
	z = get_pos_z()
	quick_print("placed", ok, "z", z, "ground", get_ground_type(), "stability", get_stability(), "blocks left", num_items(Items.Block))
	if z <= last:
		quick_print("did not rise")
	last = z
