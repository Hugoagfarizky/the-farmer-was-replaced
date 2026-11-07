# Achievement: Bamboo Farmer (farm a lot of bamboo).
# Bamboo grows 1 block per second, but stops at each fruit until the fruit is plucked.
# It grows no higher than its third fruit, and harvesting it whole pays the square of its height.
#
# Layout: columns repeat as bamboo, lane, bamboo. Each drone owns one lane and walks it north,
# tending the bamboo on both sides, until you stop it:
#   - no bamboo: step in, till if needed, plant, step back.
#   - before the second fruit is plucked: measure() gives the height of the next fruit. The drone
#     hovers to that height and steps in and back out. If the fruit is there it gets plucked,
#     and if it isn't there yet the drone only passes through empty air.
#   - after two fruits: wait until the bamboo has grown to its third fruit, then hover(0) and step in
#     to harvest the whole plant, plant a new one, and step back.
# Never step into bamboo at any other height, because that harvests it from that height up.
clear()
n = get_world_size()
lanes = n // 3
d = max_drones()
if d > lanes:
	d = lanes

def back(side):
	if side == West:
		return East
	return West

def plant_here():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Bamboo)

# s = [fruits plucked, time when the bamboo is fully grown]
def tend(side, s):
	if get_entity_type(side) != Entities.Bamboo:
		move(side)
		plant_here()
		move(back(side))
		s[0] = 0
		return
	f = measure(side)
	if s[0] >= 2 or f == None:
		if s[0] < 2 or get_time() >= s[1]:
			hover(0)
			move(side)
			plant_here()
			move(back(side))
			s[0] = 0
		return
	hover(f)
	move(side)
	move(back(side))
	f2 = measure(side)
	if f2 != f:
		s[0] += 1
		if s[0] == 2:
			if f2 == None:
				s[1] = get_time() + 10
			else:
				s[1] = get_time() + (f2 - f) + 2

def worker(x):
	# Fly high on the way to the lane, so the drone doesn't hit young bamboo.
	hover(18)
	for i in range(x):
		move(East)
	state = []
	for i in range(2 * n):
		state.append([0, 0])
	while True:
		for y in range(n):
			# Clear the lane tile, so hover(0) isn't blocked by grass.
			if get_entity_type() != None:
				harvest()
			tend(West, state[2 * y])
			tend(East, state[2 * y + 1])
			move(North)

for j in range(1, d):
	spawn_drone(worker, 3 * j + 1)
worker(1)
