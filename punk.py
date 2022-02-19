# punk.py

from operator import truediv
import d20 as dice
from gear import Gear
from skirmish import Skirmish
import utils

class Punk():
    # Punk type
    MELEE_PUNK = 0
    RANGED_PUNK = 1
    
    # Modifiers
    NO_MOD = 0
    CHARGE_ATTACK_PEN = -1
    FOCUS_ATTACK_BONUS = 1
    CHARGE_SPEED_BONUS = 2
    SHOOT_MOVE_SPEED = 3

    def __init__(self, name, weapon, armour):
        self.name = name
        self.weapon = weapon
        self.armour = armour
        self.pos = 0
        self.type = self.get_type(weapon)
        self.range = self.get_range(weapon)
        self.attack = self.get_attack(weapon)
        self.damage = self.get_damage(weapon)
        self.armour = self.get_armour(armour)
        self.health = self.get_health(armour)
        self.speed = self.get_speed(armour)

    def make_attack(self, target, mod):
        result = dice.roll("1d6+" + str(self.attack + mod)).total >= target.armour
        if result:
            target.take_damage(self.damage)
            if __debug__: print(f"{self.name}: hit, dealt {self.damage} damage to {target.name}")
            if __debug__: print(f"{self.name}: {target.name} now has {target.health} health") 
        else:
            if __debug__: print(f"{self.name}: miss")
    
    def calc_distance(self, target):
        return abs(target.pos - self.pos)
    
    def calc_direction(self, target):
        move_direction = 1
        if target.pos < self.pos:
            move_direction = -1
        return move_direction
    
    def in_range(self, target):
        dist_to_target = self.calc_distance(target)
        if __debug__: print(f"{self.name}: distance to target is {dist_to_target}")
        if dist_to_target <= self.range:
            if __debug__: print(f"{self.name}: target is in range")
            return True
        else:
            if __debug__: print(f"{self.name}: target out of range")
    
    def move(self, dist):
        if __debug__: print(f"{self.name}: old pos is {self.pos}")
        self.pos += dist
        if __debug__: print(f"{self.name}: new pos is {self.pos}")        
        
    def dash(self, target):
        if __debug__: print(f"{self.name}: dash")
        self.move(self.speed * self.calc_direction(target))
    
    def move_closer(self, target, mod):
        dist_to_target = self.calc_distance(target)
        dist = (utils.clamp(dist_to_target - self.range, 0, self.speed + mod)) * self.calc_direction(target)
        self.move(dist)
        
    def shoot_move(self, target, mod):
        if __debug__: print(f"{self.name}: shoot_move")
        dist_to_target = self.calc_distance(target)
        dist = (utils.clamp(dist_to_target - self.range, 0, self.SHOOT_MOVE_SPEED + mod)) * self.calc_direction(target)
        self.move(dist)
    
    def kite(self, target):
        if __debug__: print(f"{self.name}: kiting")
        self.move(self.SHOOT_MOVE_SPEED * -self.calc_direction(target))
    
    def can_fight(self, target):
        if __debug__: print(f"{self.name}: checking if can fight")
        dist_to_target = self.calc_distance(target)
        if dist_to_target <= self.speed:
            if __debug__: print(f"{self.name}: true, can fight")
            return True
        else:
            if __debug__: print(f"{self.name}: false, can't fight")
    
    def fight(self, target):
        if __debug__: print(f"{self.name}: fight")
        self.move_closer(target, self.NO_MOD)
        self.make_attack(target, self.NO_MOD)
            
    def can_charge(self, target):
        if __debug__: print(f"{self.name}: checking if can charge")
        dist_to_target = self.calc_distance(target)
        if dist_to_target <= self.speed + self.CHARGE_SPEED_BONUS:
            if __debug__: print(f"{self.name}: true, can charge")
            return True
        else:
            if __debug__: print(f"{self.name}: false, can't charge")
            
    def charge(self, target):
        if __debug__: print(f"{self.name}: charge")
        self.move_closer(target, self.CHARGE_SPEED_BONUS)
        self.make_attack(target, self.CHARGE_ATTACK_PEN)
    
    def focus(self, target):
        if __debug__: print(f"{self.name}: focus")
        self.make_attack(target, self.FOCUS_ATTACK_BONUS)

    def can_shoot(self, target):
        if __debug__: print(f"{self.name}: checking if can shoot")
        dist_to_target = self.calc_distance()
        if dist_to_target <= self.range + self.SHOOT_MOVE_SPEED:
            if __debug__: print(f"{self.name}: true, can shoot")
            return True
            
    def can_fight(self, target):
        if __debug__: print(f"{self.name}: checking if can fight")
        dist_to_target = self.calc_distance(target)
        if dist_to_target <= self.speed:
            if __debug__: print(f"{self.name}: true, can fight")
            return True
        else:
            if __debug__: print(f"{self.name}: false, can't fight")

    def shoot(self, target):
        if __debug__: print(f"{self.name}: shoot")
        self.make_attack(target, self.NO_MOD)
                
    def choose_action(self, target):
        if __debug__: print(f"*** {self.name.upper()} CHOOSING ACTION ***")
        if __debug__: print(f"{self.name}: my type is {self.type}")
        if __debug__: print(f"{self.name}: my pos is {self.pos}")
        if __debug__: print(f"{self.name}: target pos is {target.pos}")
        if self.type is Punk.MELEE_PUNK:
            if self.in_range(target):
                self.focus(target)
            else:
                if self.can_fight(target):
                    self.fight(target)
                elif self.can_charge(target):
                    self.charge(target)
                else:
                    self.dash(target)
        elif self.type is self.RANGED_PUNK:
            if self.in_range(target):
                self.shoot(target)
                self.kite(target)
            else:
                if self.calc_distance(target) <= self.range + self.SHOOT_MOVE_SPEED:
                    self.shoot_move(target, self.NO_MOD)
                    self.shoot(target)
                else:
                    self.move_closer(target, self.NO_MOD)
        else:
            if __debug__: print("No type given.")
        if __debug__: print()

    def take_damage(self, damage):
        self.health -= damage
    
    def set_pos(self, pos):
        self.pos = pos
    
    def get_type(self, weapon):
        match weapon:
            case Gear.LIGHT_MELEE:
                return self.MELEE_PUNK
            case Gear.HEAVY_MELEE:
                return self.MELEE_PUNK
            case Gear.SHORT_RANGE:
                return self.RANGED_PUNK
            case Gear.LONG_RANGE:
                return self.RANGED_PUNK

    def get_range(self, weapon):
        match weapon:
            case Gear.LIGHT_MELEE:
                return 1
            case Gear.HEAVY_MELEE:
                return 1
            case Gear.SHORT_RANGE:
                return 6
            case Gear.LONG_RANGE:
                return 9
            
    def get_attack(self, weapon):
        match weapon:
            case Gear.LIGHT_MELEE:
                return 1
            case Gear.HEAVY_MELEE:
                return 2
            case Gear.SHORT_RANGE:
                return 2
            case Gear.LONG_RANGE:
                return 3
            
    def get_damage(self, weapon):
        match weapon:
            case Gear.LIGHT_MELEE:
                return 1
            case Gear.HEAVY_MELEE:
                return 2
            case Gear.SHORT_RANGE:
                return 2
            case Gear.LONG_RANGE:
                return 3
            
    def get_armour(self, armour):
        match armour:
            case Gear.NO_ARMOUR:
                return 0
            case Gear.LIGHT_ARMOUR:
                return 2
            case Gear.MEDIUM_ARMOUR:
                return 4
            case Gear.HEAVY_ARMOUR:
                return 6
            
    def get_health(self, armour):
        match armour:
            case Gear.NO_ARMOUR:
                return 1
            case Gear.LIGHT_ARMOUR:
                return 3
            case Gear.MEDIUM_ARMOUR:
                return 5
            case Gear.HEAVY_ARMOUR:
                return 6
            
    def get_speed(self, armour):
        match armour:
            case Gear.NO_ARMOUR:
                return 7
            case Gear.LIGHT_ARMOUR:
                return 6
            case Gear.MEDIUM_ARMOUR:
                return 5
            case Gear.HEAVY_ARMOUR:
                return 4
