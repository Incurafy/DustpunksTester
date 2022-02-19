# main.py

from math import comb
from punk import Punk
from gear import Weapons, Armours
import d20 as dice

P1_START_POS = 0
P2_START_POS = 30
SIMULATIONS = 5000

def calc_avg(x, y):
    return (x / y) * 100

def make_punk(weapon, armour):
    name = weapon.get_name() + " " + armour.get_name()
    return Punk(name, weapon, armour)

def thunderdome():
    weapons = [Weapons.LIGHT_MELEE, Weapons.HEAVY_MELEE, Weapons.SHORT_RANGE, Weapons.LONG_RANGE]
    armours = [Armours.NO_ARMOUR, Armours.LIGHT_ARMOUR, Armours.MEDIUM_ARMOUR, Armours.HEAVY_ARMOUR]

    count = 0
    combos = []
    for weapon1 in weapons:
        for armour1 in armours:
            for weapon2 in weapons:
                for armour2 in armours:
                    p1 = make_punk(weapon1, armour1)
                    p2 = make_punk(weapon2, armour2)
                    reverse_name =  p2.name + p1.name
                    name = p1.name + p2.name
                    if name in combos or reverse_name in combos:
                        continue
                    simulate(weapon1, armour1, weapon2, armour2)
                    combos.append(name)
                    count += 1
    print(f"Total fights: {count}")

def simulate(weapon1, armour1, weapon2, armour2):
    p1_wins = 0
    p2_wins = 0
    
    for s in range(SIMULATIONS):
        p1 = make_punk(weapon1, armour1)
        p2 = make_punk(weapon2, armour2)
        p1.set_pos(P1_START_POS)
        p2.set_pos(P2_START_POS)
        reroll = True
        
        while reroll:
            p1_initiative = dice.roll("1d6").total
            p2_initiative = dice.roll("1d6").total
            
            if p1_initiative == p2_initiative:
                continue
            elif p1_initiative > p2_initiative:
                reroll = False
                if __debug__: print(f"{p1.name} has initiatve")
                while p1.health > 0 and p2.health > 0:
                    p1.choose_action(p2)
                    if p2.health > 0:
                        p2.choose_action(p1)
            else:
                reroll = False
                if __debug__: print(f"{p2.name} has initiatve")
                while p2.health > 0 and p1.health > 0:
                    p2.choose_action(p1)
                    if p1.health > 0:
                        p1.choose_action(p2)
                        
        if p2.health <= 0 and p1.health >= 1:
            p1_wins += 1
        elif p1.health <= 0 and p2.health >= 1:
            p2_wins += 1
      
    print(f"{p1.name} win rate: {calc_avg(p1_wins, SIMULATIONS)}% ({p1_wins}/{SIMULATIONS} simulations)")
    print(f"{p2.name} win rate: {calc_avg(p2_wins, SIMULATIONS)}% ({p2_wins}/{SIMULATIONS} simulations)")
    print()
    
thunderdome()