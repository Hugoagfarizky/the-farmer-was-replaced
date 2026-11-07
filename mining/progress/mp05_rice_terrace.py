# Achievement: Rice Terrace (plant rice, which turns the clay into a rice terrace).
# One drone digs down to the clay sheet under the dirt and keeps farming rice on that tile until you stop it.
# Rice cycle on a tile: Clay -> plant -> Rice_Terrace (growing) -> Dry_Rice_Terrace (grown)
# -> harvest -> dig the dry block -> Clay below -> plant again.
clear()
change_hat(Hats.Mining_Hat)
while True:
	if can_harvest():
		harvest()
	g = get_ground_type()
	if g == Grounds.Clay:
		plant(Entities.Rice)
	elif g != Grounds.Rice_Terrace:
		dig()
