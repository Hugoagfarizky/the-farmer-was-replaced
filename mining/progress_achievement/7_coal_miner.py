# Achievement: Coal Miner (mine a lot of coal).
# Coal sits in 1-block thick horizontal sheets inside the dirt, above the clay sheet.
# Coal only pays when the drone digs straight into it, and every dig destroys the four
# neighboring blocks at the same depth, coal included.
#
# Every drone owns a band of rows and sweeps it layer by layer, until you stop it:
#   - standing on coal: dig it, to collect the coal.
#   - on a plus center with no coal under it or next to it: dig the dirt. A dig removes
#     the four neighbors too, so centers laid out as (x + 2y) % 5 == 0 clear a whole layer
#     with only a fifth of the digs.
#   - anything else: skip it. A center next to coal waits until that coal has been mined.
#   - clay under the drone: the dirt layer is done there, so stop digging.
# When a sweep digs nothing, the band is done. Once every band is done, the farm is cleared
# and the drones start again from the surface.
n = get_world_size()
d = max_drones()
if d > n:
	d = n
h = n // d
dirs = [North, East, South, West]

def band_rows(k):
	if d == 1:
		return n
	if k == d - 1:
		return n - h * (d - 1)
	return h

def star(x, y):
	return (x % n + 2 * (y % n)) % 5 == 0

# A tile digs dirt if it is a plus center, or if no center covers it because the pattern
# doesn't wrap cleanly around the edge of the farm.
def is_center(x, y):
	if star(x, y):
		return True
	if star(x + 1, y) or star(x - 1, y) or star(x, y + 1) or star(x, y - 1):
		return False
	return True

def coal_next_to():
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Coal:
			return True
	return False

# Returns 1 when the drone dug, 0 when it skipped the tile.
def visit():
	g = get_ground_type()
	if g == Grounds.Coal:
		dig()
		return 1
	if g == Grounds.Clay:
		return 0
	if is_center(get_pos_x(), get_pos_y()) and not coal_next_to():
		dig()
		return 1
	return 0

def mine_band(y0, rows):
	change_hat(Hats.Mining_Hat)
	for i in range(y0):
		move(North)
	dug = 1
	while dug > 0:
		dug = 0
		for r in range(rows):
			for i in range(n):
				dug += visit()
				move(East)
			move(North)
		for r in range(rows):
			move(South)
	return True

while True:
	clear()
	drones = []
	for k in range(1, d):
		dr = spawn_drone(mine_band, k * h, band_rows(k))
		if dr != None:
			drones.append(dr)
	mine_band(0, band_rows(0))
	for dr in drones:
		wait_for(dr)
