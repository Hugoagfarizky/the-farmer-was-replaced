# Achievement: Bamboo (plant bamboo).
# Bamboo grows on tilled soil (Grounds.Soil) and planting it costs rice.
# The drone plants one bamboo, steps aside so it can grow, and replants it if it is ever gone, until you stop it.
clear()
till()
plant(Entities.Bamboo)
move(East)
while True:
	if get_entity_type(West) != Entities.Bamboo:
		move(West)
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Bamboo)
		move(East)
