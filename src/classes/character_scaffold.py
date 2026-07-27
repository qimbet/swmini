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
            owner,

            attacks=None,
            abilities=None,
            passive=None,
        ):

        self.cost = cost
        self.faction = faction
        self.name = name
        self.fullArt_path = fullArt_path
        self.icon_path = icon_path

        self.health = health
        self.defense = defense
        self.movement = movement
        self.detection = detection

        self.rarity = rarity
        self.owner = owner
        self.original_owner = owner

        self.attacks = attacks or [] #can append to this list to 'equip'
        self.abilities = abilities or []
        self.passive = passive or []

    def exportUnit(self):
        return {
            "cost": self.cost,
            "faction": self.faction,
            "name": self.name,

            "fullArt_path": self.fullArt_path,
            "icon_path": self.icon_path,

            "health": self.health,
            "defense": self.defense,
            "movement": self.movement,
            "detection": self.detection,

            "rarity": self.rarity,

            "attacks": self.attacks,
            "abilities": self.abilities,
            "passive": self.passive,

            # runtime state
            "position": self.position,
            "owner": self.owner,
            "original_owner": self.original_owner,
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

            health=data["health"],
            defense=data["defense"],
            movement=data["movement"],
            detection=data["detection"],

            rarity=data["rarity"],
            owner=data["owner"],
            original_owner=data["original_owner"],

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