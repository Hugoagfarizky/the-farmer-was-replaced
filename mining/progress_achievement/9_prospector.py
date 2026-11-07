# Achievement: Prospector (use prospect_iron to find iron).
# prospect_iron() costs 1 coal and returns the direction of one step toward the closest iron ore.
# It returns None when the iron is straight below the drone, so then the drone digs down toward it.
# One drone keeps prospecting and mining iron until you stop it.
# Coal and iron it lands on are mined on the way. Without coal it can't prospect, so it digs down
# and looks for iron in the four neighboring tiles instead.
clear()
change_hat(Hats.Mining_Hat)
dirs = [North, East, South, West]

def iron_next_to():
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Iron:
			return dr
	return None

while True:
	g = get_ground_type()
	if g == Grounds.Iron or g == Grounds.Coal:
		dig()
	else:
		dr = iron_next_to()
		if dr == None and num_items(Items.Coal) > 0:
			dr = prospect_iron()
		if dr == None:
			dig()
		else:
			move(dr)
