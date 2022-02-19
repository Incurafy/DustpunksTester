# main.py

from punk import Punk
from gear import Gear

def main():
    p1 = Punk("Sniper", Gear.LONG_RANGE, Gear.LIGHT_ARMOUR)
    p2 = Punk("Samurai", Gear.HEAVY_MELEE, Gear.HEAVY_ARMOUR)
    
    p1.set_pos(0)
    p2.set_pos(1)
    
    round = 0
    while p1.health > 0 and p2.health > 0:
        if p1.health > 0:
            p1.choose_action(p2)
        
        if p2.health > 0:
            p2.choose_action(p1)
        round += 1
        if __debug__: print(f"End of round: {round}\n")
        
    if p1.health <= 0:
        if __debug__: print(f"{p2.name} wins in {round} rounds")
    
    elif p2.health <= 0:
        if __debug__: print(f"{p1.name} wins in {round} rounds")
    
main()
