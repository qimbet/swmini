from re import I

from src.classes.attacks import *
from src.classes.abilities import *


class Unit:
    def __init__(
            self,
            cost,
            faction,
            name,
            fullArt_path,
            icon_path,

            health,
            defense,
            movement,
            detection,

            rarity,

            attacks=None,
            abilities=None,
            passive=None,

        ):

        cost = self.cost,
        faction = self.faction,
        name = self.name,
        fullArt_path = self.fullArt_path,
        icon_path = self.icon_path,

        health = self.health,
        defense = self.defense,
        movement = self.movement,
        detection = self.detection,

        rarity = self.rarity,

        self.attacks = self.attacks or [] #can append to this list to 'equip'
        self.abilities = self.abilities or []
        self.passive = self.passive or []



#instantiate character using:
#marine = Unit(
    #name="sniper",
    #**UNIT_DATA["sniper"]
#)