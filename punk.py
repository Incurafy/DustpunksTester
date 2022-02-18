# punk.py

import d20 as dice
import utils

class Punk():   
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

   # Modifiers
    NO_MOD = 0
    CHARGE_ATTACK_PEN = -1
    FOCUS_ATTACK_BONUS = 1
    CHARGE_MOVE_BONUS = 2
    SHOOT_MOVE_SPEED = 3

    def __init__(self, name, weapon, armour, pos) -> None:
        self.name = name
        self.weapon = weapon
        self.armour = armour
        self.pos = pos
        self.range = self.get_range(weapon)
        self.attack = self.get_attack(weapon)
        self.damage = self.get_damage(weapon)
        self.armour = self.get_armour(armour)
        self.health = self.get_health(armour)
        self.speed = self.get_speed(armour)
        
    def make_attack(self, target, mod):
        result = dice.roll("1d6+" + str(self.attack + mod)).total >= target.armour
        if result:
            target.set_health(target.health - self.damage)
    
    def calc_distance(self, target):
        return abs(target.pos - self.pos)
    
    def calc_direction(self, target):
        move_direction = 1
        if target.pos < self.pos:
            move_direction = -1
        return move_direction
    
    def move(self, dist):
        self.pos += dist
        
    def dash(self):
        self.move(self.speed)
    
    def move_closer(self, target, mod):
        dist_to_target = self.calc_distance(target)
        dist = (utils.clamp(dist_to_target - self.range, 0, self.speed + mod)) * self.calc_direction(target)
        self.move(dist)
    
    def kite(self, target):
        self.move(self.SHOOT_MOVE_SPEED * -self.calc_direction(target))
    
    def fight(self, target):
        active = True
        dist_to_target = self.calc_distance(target)
        while active:
            if dist_to_target <= self.range:
                self.make_attack(target, self.NO_MOD)
                active = False
            else:
                self.move_closer(target, self.NO_MOD)
                if self.range < dist_to_target:
                    active = False
                    
    def charge(self, target):
        self.move_closer(self.calc_distance(target), self.CHARGE_MOVE_BONUS)
        self.make_attack(target, self.CHARGE_ATTACK_PEN)
    
    def focus(self, target):
        self.make_attack(target, self.FOCUS_ATTACK_BONUS)

    def shoot(self, target):
        dist_to_target = self.calc_distance(target)
        active = True
        while active:
            if dist_to_target <= self.range:
                self.make_attack(target, self.NO_MOD)
                self.kite(target)
                active = False
            else:
                self.move_closer(target, self.NO_MOD)
                if dist_to_target <= self.range:
                    self.make_attack(target, self.NO_MOD)
                active = False

    def get_range(self, weapon):
        match weapon:
            case self.LIGHT_MELEE:
                return 1
            case self.HEAVY_MELEE:
                return 1
            case self.SHORT_RANGE:
                return 6
            case self.LONG_RANGE:
                return 9
            
    def get_attack(self, weapon):
        match weapon:
            case self.LIGHT_MELEE:
                return 1
            case self.HEAVY_MELEE:
                return 2
            case self.SHORT_RANGE:
                return 2
            case self.LONG_RANGE:
                return 3
            
    def get_damage(self, weapon):
        match weapon:
            case self.LIGHT_MELEE:
                return 1
            case self.HEAVY_MELEE:
                return 2
            case self.SHORT_RANGE:
                return 2
            case self.LONG_RANGE:
                return 3
            
    def get_armour(self, armour):
        match armour:
            case self.NO_ARMOUR:
                return 0
            case self.LIGHT_ARMOUR:
                return 2
            case self.MEDIUM_ARMOUR:
                return 4
            case self.HEAVY_ARMOUR:
                return 6
            
    def get_health(self, armour):
        match armour:
            case self.NO_ARMOUR:
                return 1
            case self.LIGHT_ARMOUR:
                return 3
            case self.MEDIUM_ARMOUR:
                return 5
            case self.HEAVY_ARMOUR:
                return 6
            
    def set_health(self, new_health):
        self.health = new_health
            
    def get_speed(self, armour):
        match armour:
            case self.NO_ARMOUR:
                return 7
            case self.LIGHT_ARMOUR:
                return 6
            case self.MEDIUM_ARMOUR:
                return 5
            case self.HEAVY_ARMOUR:
                return 4
