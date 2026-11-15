# Achievement: Place (place a block).
# place(ground) puts a block under the drone, on top of the column it is over.
# The drone places one red block, then does flips until you stop it.
clear()
place(Grounds.Block_Red)
while True:
	do_a_flip()
