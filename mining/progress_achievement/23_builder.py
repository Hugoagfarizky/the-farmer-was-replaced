# Achievement: Builder (place 1,000 blocks).
# Every drone owns a band of rows and places one colored block on each tile per pass, in a
# red, green, blue pattern, until you stop it. The whole farm rises one layer per pass, so the
# columns stay level and nothing caves in. 23_builder, 24_big_builder, and 26_picasso run the same
# code, so running one of them long enough can earn all three.
clear()
n = get_world_size()
d = max_drones()
if d > n:
	d = n
h = n // d
colors = [Grounds.Block_Red, Grounds.Block_Green, Grounds.Block_Blue]

def band_rows(k):
	if d == 1:
		return n
	if k == d - 1:
		return n - h * (d - 1)
	return h

def worker(y0, rows):
	for i in range(y0):
		move(North)
	while True:
		for r in range(rows):
			for i in range(n):
				place(colors[(get_pos_x() + get_pos_y()) % 3])
				move(East)
			move(North)
		for r in range(rows):
			move(South)

for k in range(1, d):
	spawn_drone(worker, k * h, band_rows(k))
worker(0, band_rows(0))
