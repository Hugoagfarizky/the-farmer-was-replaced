# Achievement: Skyscraper (place a block to reach the height of +150 z).
# A single tall tower caves in, because a block falls when a neighboring column is more than its
# stability lower. So this builds a pyramid instead, until you stop it:
#   1. Place one blue block in the middle of the farm and read its stability s.
#   2. Each tile's target height is the peak height minus s times its distance from the middle,
#      so neighboring tiles never differ by more than s.
#   3. All drones raise every tile one layer per pass, then wait for each other before the next pass.
#      Tiles stop at their target height, so the pyramid always stays within its stability.
#   4. After the peak passes +150 z it keeps doing passes, which repair anything that caved in.
# The stability, the peak height, and the progress go to output.txt.
clear()
n = get_world_size()
d = max_drones()
if d > n:
	d = n
h = n // d
c = n // 2

for i in range(c):
	move(East)
	move(North)
z0 = get_pos_z()
place(Grounds.Block_Blue)
s = get_stability()
goal = 150 - z0 + 1
quick_print("surface z", z0, "block stability", s, "peak blocks", goal, "world", n, "drones", d)
for i in range(c):
	move(West)
	move(South)

def band_rows(k):
	if d == 1:
		return n
	if k == d - 1:
		return n - h * (d - 1)
	return h

def gap(a, b):
	g = a - b
	if g < 0:
		g = -g
	if g > n - g:
		g = n - g
	return g

def target(x, y):
	dx = gap(x, c)
	dy = gap(y, c)
	if s < 1:
		return goal
	t = goal - s * (dx + dy)
	if t < 0:
		return 0
	return t

def one_pass(y0, rows, p):
	for i in range(y0):
		move(North)
	for r in range(rows):
		y = get_pos_y()
		if target(c, y) > 0:
			for i in range(n):
				t = target(get_pos_x(), y)
				if t > p:
					t = p
				if get_pos_z() < z0 + t:
					place(Grounds.Block_Blue)
				move(East)
		move(North)
	for r in range(y0 + rows):
		move(South)
	return True

p = 1
while True:
	drones = []
	for k in range(1, d):
		dr = spawn_drone(one_pass, k * h, band_rows(k), p)
		if dr != None:
			drones.append(dr)
	one_pass(0, band_rows(0), p)
	for dr in drones:
		wait_for(dr)
	if p % 10 == 0 or p == goal:
		quick_print("pass", p, "blocks", num_items(Items.Block))
	if p < goal:
		p += 1
