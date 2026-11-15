# Achievement: Mushroom (find a mushroom).
# Mushrooms grow in a stratum of Grounds.Mushroom underground.
# One drone digs down until it stands on a mushroom block, then does flips until you stop it.
clear()
change_hat(Hats.Mining_Hat)
while get_ground_type() != Grounds.Mushroom:
	dig()
while True:
	do_a_flip()
