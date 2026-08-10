from src.classes.attacks import *
from src.classes.abilities import *

from dataclasses import dataclass

@dataclass
class Footprint:
    width: int
    length: int

class Unit:
    def __init__( #better to pass these as a dict; later unpacked
            self,
            cost,
            faction,
            name,

            health,
            defense,
            movement,
            detection_range,

            rarity,
            owner,
            footprint,

            attacks=None,
            abilities=None,
            passive=None,

            symbol=None,
            fullArt_path=None,
            icon_path=None,
        ):

        self.cost = cost
        self.faction = faction
        self.name = name

        self.fullArt_path = fullArt_path
        self.icon_path = icon_path
        self.symbol = symbol

        self.position = None
        self.footprint =  footprint

        self.health = health
        self.current_health = health 
        self.defense = defense
        self.movement = movement
        self.detection_range = detection_range

        self.rarity = rarity
        self.owner = owner

        self.attacks = attacks or [] #can append to this list to 'equip'
        self.abilities = abilities or []
        self.passive = passive or []

    
    def occupied_positions(self, position=None):
        """
        Return all map cells occupied by this unit.
        position is the top-left/anchor position.
        """
        if position is None:
            position = self.position

        if position is None:
            return []

        x, y = position
        length = self.footprint.length
        width = self.footprint.width

        return [
            (x + dx, y + dy)
            for dy in range(length)
            for dx in range(width)
        ]


    def exportUnit(self):
        return {
            "cost": self.cost,
            "faction": self.faction,
            "name": self.name,

            "fullArt_path": self.fullArt_path,
            "icon_path": self.icon_path,
            "symbol": self.symbol,

            "health": self.health,
            "current_health": self.current_health,
            "defense": self.defense,
            "movement": self.movement,
            "detection_range": self.detection_range,

            "footprint": self.footprint,

            "rarity": self.rarity,

            "attacks": self.attacks,
            "abilities": self.abilities,
            "passive": self.passive,

            # runtime state
            "position": self.position,
            "owner": self.owner,
            "status_effects": self.status_effects,
            "cooldowns": self.cooldowns,
        }
        
    @classmethod
    def import_unit(cls, data):

        unit = cls(
            cost=data["cost"],
            faction=data["faction"],
            name=data["name"],

            fullArt_path=data.get("fullArt_path"),
            icon_path=data.get("icon_path"),
            symbol=data.get("symbol"),

            health=data["health"],
            current_health=data["current_health"],
            defense=data["defense"],
            movement=data["movement"],
            detection_range=data["detection_range"],

            footprint=data["footprint"],

            rarity=data["rarity"],
            owner=data["owner"],

            attacks=data["attacks"],
            abilities=data["abilities"],
            passive=data["passive"],
        )

        unit.position = data.get("position")
        unit.status_effects = data.get("status_effects",[])
        unit.cooldowns = data.get("cooldowns", {})

        return unit

#instantiate character using:
#marine = Unit(
    #name="sniper",
    #**UNIT_DATA["sniper"]
#)