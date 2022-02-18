# main.py

from punk import Punk
import d20 as dice

# Weapons
LIGHT_MELEE = 0
HEAVY_MELEE = 1
SHORT_RANGE = 2
LONG_RANGE = 3

# Armour
NO_ARMOUR = 4
LIGHT_ARMOUR = 5
MEDIUM_ARMOUR = 6
HEAVY_ARMOUR = 7

def main():
    map = [i for i in range (0, 24)]
    p1 = Punk("Sniper", LONG_RANGE, LIGHT_ARMOUR, 0)
    p2 = Punk("Samurai", HEAVY_MELEE, HEAVY_ARMOUR, len(map)-1)
    count = 0
    reroll = True
    
    def print_map(map, p1, p2):
        for x in range(len(map)):
            map[x] = "_"
        if p1.health > 0:
            map[p1.pos] = "1"
        if p2.health > 0:
            map[p2.pos] = "2"
        print(str(map) + "\n")
    
    while reroll:
        print_map(map, p1, p2)
        p1_initiative = dice.roll("1d6").total
        p2_initiative = dice.roll("1d6").total
        
        if p1_initiative == p2_initiative:
            print("Rolled the same, re-rolling")
            continue
        elif p1_initiative > p2_initiative:
            print(f"{p1.name} has initiative\n")
            reroll = False
            while p1.health > 0 and p2.health > 0:
                count += 1
                p1.shoot(p2)
                if p2.health > 0:
                    p2.fight(p1)
                print_map(map, p1, p2)
        else:
            print(f"{p2.name} has initiative\n")
            reroll = False
            while p2.health > 0 and p1.health > 0:
                count += 1
                p2.fight(p1)
                if p1.health > 0:
                    p1.shoot(p2)
                print_map(map, p1, p2)

    if p1.health <= 0:
        print(f"{p2.name} victory on round {count}")
    if p2.health <= 0:
        print(f"{p1.name} victory on round {count}")
    
main()