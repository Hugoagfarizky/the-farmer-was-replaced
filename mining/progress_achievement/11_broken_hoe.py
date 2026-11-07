# Achievement: Broken Hoe (till rock).
# Grounds.Rock lies below the dirt and the clay sheet. One drone digs down until it stands on rock,
# then keeps calling till() on it, digging again whenever the ground under it isn't rock, until you stop it.
clear()
change_hat(Hats.Mining_Hat)
while True:
	if get_ground_type() == Grounds.Rock:
		till()
	else:
		dig()
