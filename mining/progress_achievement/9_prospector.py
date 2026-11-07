# Achievement: Prospector (use prospect_iron to find iron).
# prospect_iron() costs 1 coal and returns the direction of one step toward the closest iron ore.
# It returns None when the iron is straight below the drone, so then the drone digs down toward it.
# It also returns None when there is no iron in range or no coal left, and the drone digs down then too.
# One drone keeps prospecting and mining iron until you stop it.
clear()
change_hat(Hats.Mining_Hat)
while True:
	dr = prospect_iron()
	if dr == None:
		dig()
	else:
		move(dr)
