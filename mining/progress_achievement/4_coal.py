# Achievement: Coal (mine a coal block).
# Digs straight down and mines every coal block it lands on, until you stop it.
# Before and after each coal dig it prints the ground in the four neighboring tiles,
# to show whether neighboring coal is lost when the drone mines a coal block.
clear()
change_hat(Hats.Mining_Hat)

def around():
	return [get_ground_type(North), get_ground_type(East), get_ground_type(South), get_ground_type(West)]

while True:
	if get_ground_type() == Grounds.Coal:
		print("before", get_pos_z(), around())
		dig()
		print("after", get_pos_z(), get_ground_type(), around())
	else:
		dig()
