# Achievement: Quartz (mine a quartz block).
# Quartz grows in vertical needles in the lower part of Grounds.Rock and the hard dirt below it.
# prospect_quartz() costs 1 iron and returns the 3D distance to the closest quartz block (None if none is near).
#
# One drone digs down to the rock, then walks toward the closest needle while digging, until you stop it:
#   - standing on quartz or iron: dig it.
#   - quartz in a neighboring tile: step onto it.
#   - otherwise: step one tile in the current heading and prospect again. If the distance went down,
#     stay there, otherwise step back and turn. Then dig one block.
# Digging removes the four neighboring blocks, so the neighbors are always as deep as the drone
# and it can step sideways without climbing back up. Each dig pulls the next ring down too.
clear()
change_hat(Hats.Mining_Hat)
dirs = [North, East, South, West]

def quartz_next_to():
	for dr in dirs:
		if get_ground_type(dr) == Grounds.Quartz:
			return dr
	return None

while get_ground_type() != Grounds.Rock:
	dig()

heading = 0
while True:
	g = get_ground_type()
	if g == Grounds.Quartz or g == Grounds.Iron:
		dig()
		continue
	q = quartz_next_to()
	if q != None:
		move(q)
		continue
	dist = prospect_quartz()
	if dist == None:
		for i in range(5):
			dig()
		continue
	for t in range(4):
		move(dirs[heading])
		d2 = prospect_quartz()
		if d2 != None and d2 < dist:
			break
		move(dirs[(heading + 2) % 4])
		heading = (heading + 1) % 4
	dig()
