# Achievement: Dynamite Miner (mine 1,000 dynamite).
# Same Minesweeper solver as 29_dynamite_disposal, on the full farm, since a bigger farm has more
# dynamite to collect. Every dud dug pays a bit of dynamite, and a solved stratum also pays the
# number of fully uncovered live blocks, squared. Until you stop it:
#   1. All drones dig every tile down to the dynamite layer, never into it.
#   2. One drone digs the middle tile (the first dig is always a dud), then keeps digging tiles
#      that are proven safe. When nothing is proven safe, it guesses the least risky tile.
#   3. Solved or blown up, the farm is cleared and a new round starts.
# Every round's result goes to output.txt.
n = get_world_size()
N = n * n
d = max_drones()
if d > n:
	d = n
h = n // d

def band_rows(k):
	if d == 1:
		return n
	if k == d - 1:
		return n - h * (d - 1)
	return h

# Phase 1: every drone digs every tile of its band down to the dynamite layer, never into it.
def lower_band(y0, rows):
	change_hat(Hats.Mining_Hat)
	for i in range(y0):
		move(North)
	for r in range(rows):
		for i in range(n):
			g = get_ground_type()
			while g != Grounds.Dynamite and g != Grounds.Soot and get_pos_z() > -5000:
				dig()
				g = get_ground_type()
			move(East)
		move(North)
	for r in range(y0 + rows):
		move(South)
	return True

def lower_farm():
	drones = []
	for k in range(1, d):
		dr = spawn_drone(lower_band, k * h, band_rows(k))
		if dr != None:
			drones.append(dr)
	lower_band(0, band_rows(0))
	for dr in drones:
		wait_for(dr)

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

# Phase 2: Minesweeper on the dynamite layer.
# state: 0 unknown, 1 dug (its soot number is known), 2 live, 3 known safe but not dug yet.
# The soot counts are assumed not to wrap around the farm edge. If an edge tile ever counts more
# live neighbors than it has inside the farm, the counts do wrap, and the neighbor lists switch over.
wrap = [False]

def neighbors(i):
	x = i % n
	y = i // n
	out = []
	for dy in [-1, 0, 1]:
		for dx in [-1, 0, 1]:
			if dx != 0 or dy != 0:
				nx = x + dx
				ny = y + dy
				if wrap[0]:
					out.append((ny % n) * n + nx % n)
				elif nx >= 0 and nx < n and ny >= 0 and ny < n:
					out.append(ny * n + nx)
	return out

def build_nb():
	nb = []
	for i in range(N):
		nb.append(neighbors(i))
	return nb

def unknowns(i, nb, state):
	u = []
	f = 0
	for j in nb[i]:
		if state[j] == 0:
			u.append(j)
		elif state[j] == 2:
			f += 1
	return [u, f]

# Simple rules: a number already met by known live tiles makes the rest safe,
# and a number that needs every unknown neighbor makes them all live.
def simple(nb, state, num):
	changed = False
	for i in range(N):
		if state[i] == 1:
			uf = unknowns(i, nb, state)
			u = uf[0]
			if len(u) > 0:
				r = num[i] - uf[1]
				if r == 0:
					for j in u:
						state[j] = 3
					changed = True
				elif r == len(u):
					for j in u:
						state[j] = 2
					changed = True
	return changed

# Subset rule: if A's unknown neighbors are all also B's, the extra ones in B hold
# exactly B's remaining count minus A's.
def subset(nb, state, num):
	for a in range(N):
		if state[a] == 1:
			ufa = unknowns(a, nb, state)
			ua = ufa[0]
			if len(ua) > 0:
				ra = num[a] - ufa[1]
				seen = set()
				for j in ua:
					for b in nb[j]:
						if b != a and state[b] == 1 and not (b in seen):
							seen.add(b)
							ufb = unknowns(b, nb, state)
							ub = ufb[0]
							inside = True
							for x in ua:
								if not (x in ub):
									inside = False
							if inside and len(ub) > len(ua):
								rest = []
								for x in ub:
									if not (x in ua):
										rest.append(x)
								rr = num[b] - ufb[1] - ra
								if rr == 0:
									for x in rest:
										state[x] = 3
									return True
								if rr == len(rest):
									for x in rest:
										state[x] = 2
									return True
	return False

# When nothing is certain, dig the unknown tile with the lowest chance of being live.
def guess(nb, state, num):
	best = None
	bp = 2.0
	for j in range(N):
		if state[j] == 0:
			p = 0.15
			for i in nb[j]:
				if state[i] == 1:
					uf = unknowns(i, nb, state)
					q = (num[i] - uf[1]) / len(uf[0])
					if q > p or p == 0.15:
						p = q
			if p < bp:
				bp = p
				best = j
	quick_print("  guess", best % n, best // n, "risk", bp)
	return best

def nearest(state):
	best = None
	bd = N * 2
	x0 = get_pos_x()
	y0 = get_pos_y()
	for j in range(N):
		if state[j] == 3:
			dx = (j % n - x0) % n
			if dx > n - dx:
				dx = n - dx
			dy = (j // n - y0) % n
			if dy > n - dy:
				dy = n - dy
			if dx + dy < bd:
				bd = dx + dy
				best = j
	return best

# Returns True when the puzzle is solved, False when live dynamite went off.
def solve():
	nb = build_nb()
	state = []
	num = []
	for i in range(N):
		state.append(0)
		num.append(0)
	j = (n // 2) * n + n // 2
	while True:
		goto(j % n, j // n)
		if get_ground_type() == Grounds.Dynamite:
			dig()
		if get_ground_type() != Grounds.Soot:
			quick_print("  exploded at", j % n, j // n)
			return False
		v = measure()
		if v == None:
			return True
		state[j] = 1
		num[j] = v
		if not wrap[0] and v > len(nb[j]):
			wrap[0] = True
			nb = build_nb()
			quick_print("  counts wrap around the edge")
		j = nearest(state)
		while j == None:
			if simple(nb, state, num):
				j = nearest(state)
			elif subset(nb, state, num):
				j = nearest(state)
			else:
				j = guess(nb, state, num)
				if j == None:
					quick_print("  no unknown tiles left but not solved")
					return False

rounds = 0
while True:
	clear()
	lower_farm()
	rounds += 1
	quick_print("round", rounds, "dynamite layer at z", get_pos_z())
	quick_print("round", rounds, "solved", solve(), "dynamite", num_items(Items.Dynamite))
