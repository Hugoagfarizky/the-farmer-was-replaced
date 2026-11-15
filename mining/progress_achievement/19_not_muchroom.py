# Achievement: Not Muchroom (try and fail to push a mushroom).
# A push fails when another block is in the way. Right after the drone digs down onto the mushroom
# stratum, the blocks next to it are still there, so pushing sideways fails.
# One drone digs down to the mushroom stratum and keeps trying to push in every direction until you stop it.
clear()
change_hat(Hats.Mining_Hat)
dirs = [North, East, South, West]
while True:
	if get_ground_type() != Grounds.Mushroom:
		dig()
	else:
		for dr in dirs:
			push(dr)
