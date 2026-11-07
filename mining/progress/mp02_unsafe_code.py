# Achievement: Unsafe Code (unequip the mining helmet and keep digging).
# Digs once with the mining helmet, swaps it for the straw hat, then keeps digging until you stop it.
clear()
change_hat(Hats.Mining_Hat)
dig()
change_hat(Hats.Straw_Hat)
while True:
	dig()
