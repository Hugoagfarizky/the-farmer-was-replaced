# Achievement: Dynamite (find a dynamite layer).
# One drone digs down until it stands on Grounds.Dynamite, then does flips until you stop it.
# It never digs the dynamite itself, because live dynamite explodes.
clear()
change_hat(Hats.Mining_Hat)
while get_ground_type() != Grounds.Dynamite:
	dig()
while True:
	do_a_flip()
