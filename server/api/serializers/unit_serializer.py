def _serialize_footprint(footprint):
    """
    Serialize a Unit Footprint into an API-safe dictionary.
    """

    if footprint is None:
        return None

    return {
        "width": footprint.width,
        "length": footprint.length,
    }


def _serialize_position(position):
    """
    Convert a tuple/list position into a JSON-safe list.

    None remains None.
    """

    if position is None:
        return None

    return list(position)


def _serialize_attack(attack):
    """
    Convert an attack object into an API-safe representation.

    Until attacks have an explicit serializer, prefer an object's
    export() method when available, otherwise fall back to its
    __dict__.

    This is intentionally isolated so attack serialization can be
    replaced later without changing unit serialization.
    """

    if hasattr(attack, "export"):
        return attack.export()

    if hasattr(attack, "__dict__"):
        return dict(attack.__dict__)

    return attack


def _serialize_ability(ability):
    """
    Convert an ability object into an API-safe representation.

    This follows the same strategy as attacks and can be replaced
    with a dedicated ability serializer later.
    """

    if hasattr(ability, "export"):
        return ability.export()

    if hasattr(ability, "__dict__"):
        return dict(ability.__dict__)

    return ability


def _serialize_passive(passive):
    """
    Convert a passive object into an API-safe representation.
    """

    if hasattr(passive, "export"):
        return passive.export()

    if hasattr(passive, "__dict__"):
        return dict(passive.__dict__)

    return passive


def serialize_unit(unit):
    """
    Serialize a live Unit into an API-safe dictionary.

    Object references such as owner are represented by IDs rather
    than serializing the Python object itself.
    """

    owner_id = None

    if unit.owner is not None:
        owner_id = unit.owner.id

    return {
        "unit_id": unit.id,

        # Identity / definition
        "name": unit.name,
        "faction": unit.faction,
        "rarity": unit.rarity,
        "cost": unit.cost,
        "symbol": unit.symbol,

        # Presentation metadata
        "fullArt_path": unit.fullArt_path,
        "icon_path": unit.icon_path,

        # Physical characteristics
        "footprint": _serialize_footprint(unit.footprint),

        # Combat characteristics
        "health": unit.health,
        "current_health": unit.current_health,
        "defense": unit.defense,
        "movement": unit.movement,
        "detection_range": unit.detection_range,

        # Runtime state
        "position": _serialize_position(unit.position),
        "owner_id": owner_id,
        "status_effects": list(unit.status_effects),
        "cooldowns": dict(unit.cooldowns),

        # Equipment / capabilities
        "attacks": [
            _serialize_attack(attack)
            for attack in unit.attacks
        ],

        "abilities": [
            _serialize_ability(ability)
            for ability in unit.abilities
        ],

        "passive": [
            _serialize_passive(passive)
            for passive in unit.passive
        ],
    }


def serialize_units(units):
    """
    Serialize a collection of live units.

    Returns a list suitable for inclusion in the game-state payload.
    """

    return [
        serialize_unit(unit)
        for unit in units
    ]