# gear.py

from enum import Enum

class Weapons(Enum):
    LIGHT_MELEE = 0
    HEAVY_MELEE = 1
    SHORT_RANGE = 2
    LONG_RANGE = 3
    
    def get_name(self):
        match self:
            case Weapons.LIGHT_MELEE:
                return "Light Melee"
            case Weapons.HEAVY_MELEE:
                return "Heavy Melee"
            case Weapons.SHORT_RANGE:
                return "Short Range"
            case Weapons.LONG_RANGE:
                return "Long Range"
            case _:
                return "Hentai Cannon"

class Armours(Enum):
    NO_ARMOUR = 0
    LIGHT_ARMOUR = 1
    MEDIUM_ARMOUR = 2
    HEAVY_ARMOUR = 3
    
    def get_name(self):
        match self:
            case Armours.NO_ARMOUR:
                return "No Armour"
            case Armours.LIGHT_ARMOUR:
                return "Light Armour"
            case Armours.MEDIUM_ARMOUR:
                return "Medium Arour"
            case Armours.HEAVY_ARMOUR:
                return "Heavy Armour"
            case _:
                return "Squid Skin"
