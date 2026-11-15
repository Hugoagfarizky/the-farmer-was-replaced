# Achievement: Skyscraper (place a block to reach the height of +150 z).
# The game refuses to place a block too far above the farm's average height (a single pillar
# stopped a little past z 70 on the full farm). So this shrinks the farm to 3x3 with
# set_world_size(3), which only lasts while the program runs, and raises all 9 tiles together.
# Nine drones, one per tile, each stack rock (stability 3) on their own tile at the same pace,
# so the average rises with them and nothing caves in. They stop at z 155 and then do flips
# until you stop the program.
set_world_size(3)
clear()

def tower(x, y):
	for i in range(x):
		move(East)
	for i in range(y):
		move(North)
	while get_pos_z() < 155:
		place(Grounds.Rock)
	while True:
		do_a_flip()

for x in range(3):
	for y in range(3):
		if x > 0 or y > 0:
			spawn_drone(tower, x, y)
tower(0, 0)
