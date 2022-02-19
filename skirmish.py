# skirmish.py

# What do I actually want:
# Every combination of punks versus every other combination of punks
# Average moves
# Average attacks
# Average misses
# Average TOTAL moves
# Average TOTAL attacks
# Average TOTAL misses

""" 
*** MELEE ACTION LOGIC ***
while active
    if enemy is in range
        focus()
        active = false
    else (enemy isn't in range)
        if can_fight
            move_closer()
            fight()
            active = false
        elif can_charge
            charge()
            make_attack(with charge pen)
            active false
        else
            dash()
            active = false
            
*** RANGED ACTION LOGIC ***
while active
    if enemy is in range
        shoot()
        kite()
        active = false
    else
        move_closer()
        active = false
"""

class Skirmish:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2