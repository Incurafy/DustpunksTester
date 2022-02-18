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
    
    def calc_distance(self, target_pos, current_pos):
        return abs(target_pos - current_pos)

    def make_attack(self, target_armour):
        return dice.roll("1d6+" + str(self.attack)).total >= target_armour
    
    def move(self, dist):
        self.pos += dist
    
    def fight(self, target):
        active = True
        dist_to_target = self.calc_distance(target.pos, self.pos)
        while active:
            # If target is in range
            if dist_to_target <= self.range:
                # Attack it
                if self.make_attack(target.armour):
                    target.health -= self.damage
                else:
                    print("Miss")
                active = False
            else:
                # Move closer
                move_direction = 1
                if target.pos < self.pos:
                    move_direction = -1
                dist = (utils.clamp(dist_to_target - self.range, 0, self.speed)) * move_direction
                self.move(dist)
                dist_to_target = self.calc_distance(target.pos, self.pos)
                # If still not in range, end turn
                if self.range < dist_to_target:
                    active = False

    def shoot(self, target):
        shoot_move_speed = 3
        dist_to_target = self.calc_distance(target.pos, self.pos)
        active = True
        while active:
            # If target is in range
            if dist_to_target <= self.range:
                # Shoot it
                if self.make_attack(target.armour):
                    target.health -= self.damage
                # Run away
                move_direction = 1
                if target.pos < self.pos:
                    move_direction = -1
                self.move(shoot_move_speed * -move_direction)
                active = False
            else:
                # Move closer
                move_direction = 1
                if target.pos < self.pos:
                    move_direction = -1
                dist = (utils.clamp(dist_to_target - self.range, 0, shoot_move_speed)) * move_direction
                self.move(dist)
                dist_to_target = self.calc_distance(target.pos, self.pos)
                # If target is in range
                if dist_to_target <= self.range:
                    # Shoot it
                    if self.make_attack(target.armour):
                        target.health -= self.damage
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
