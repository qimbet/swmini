"""
Game-state serialization.

This module is the API-facing representation of the authoritative
Game state.

Important design principles:

1. Never expose live Python objects.
2. Relationships are represented by stable game-instance IDs.
3. The serialized structure should be JSON-safe.
4. API consumers should not need to understand backend classes.
5. Serialization should be read-only; it must not mutate game state.
"""

from enum import Enum


# ============================================================
# Generic helpers
# ============================================================

def _serialize_position(position):
    """
    Convert a tuple/list position into a JSON-safe list.

    None remains None.
    """
    if position is None:
        return None

    return list(position)


def _serialize_object(value):
    """
    Best-effort conversion for objects that have not yet received
    dedicated serializers.

    This should be treated as transitional infrastructure.

    As attacks, abilities, passives, status effects, etc. become
    more sophisticated, give each one its own serializer.
    """

    if value is None:
        return None

    if isinstance(value, Enum):
        return value.name

    if hasattr(value, "export"):
        return value.export()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


# ============================================================
# Map serialization
# ============================================================

def serialize_feature(feature):
    """
    Serialize a TileFeature into an API-safe representation.

    Features are represented by their type and gameplay-relevant
    properties rather than by serializing the Python object.
    """

    movement_cost = feature.movement_cost()

    if movement_cost == float("inf"):
        movement_cost = None

    data = {
        "type": feature.__class__.__name__,
        "symbol": feature.symbol(),
        "tags": list(getattr(feature, "tags", set())),
        "blocks_movement": feature.blocks_movement(),
        "movement_cost": movement_cost,
    }

    if hasattr(feature, "cover_value"):
        data["cover_value"] = feature.cover_value()

    if hasattr(feature, "height"):
        data["height"] = feature.height()

    if hasattr(feature, "blocks_vision"):
        data["blocks_vision"] = feature.blocks_vision()

    return data


def serialize_tile(tile):
    """
    Serialize a single map tile.
    """

    return {
        "features": [
            serialize_feature(feature)
            for feature in tile.features
        ],
        "no_stop": tile.no_stop,
    }


def serialize_edges(game_map):
    """
    Serialize map edges as connections between two cells.

    Edge endpoints are intentionally unordered.
    """

    edges = []

    for edge_key, edge in game_map.edges.items():

        endpoints = [
            list(position)
            for position in edge_key
        ]

        edges.append({
            "cells": endpoints,

            "type": (
                edge.edge_type.name
                if hasattr(edge.edge_type, "name")
                else str(edge.edge_type)
            ),

            "blocks_movement": edge.blocks_movement(),
            "diagonal": edge.is_diagonal(),
        })

    return edges


def serialize_map(game_map):
    """
    Serialize the complete runtime map state.
    """

    if game_map is None:
        return None

    return {
        "width": game_map.width,
        "height": game_map.height,

        "tiles": [
            [
                serialize_tile(tile)
                for tile in row
            ]
            for row in game_map.tiles
        ],

        "edges": serialize_edges(game_map),

        "reserved_positions": [
            list(position)
            for position in game_map.reserved_positions
        ],

        "spawn_parameters": game_map.spawn_parameters,

        "placed_obstacles": game_map.placed_obstacles,
    }


# ============================================================
# Player serialization
# ============================================================

def serialize_player(player):
    """
    Serialize a Player into an API-safe dictionary.

    Army composition is represented through unit IDs and original
    deployment positions.

    Live Unit objects are intentionally not embedded here.
    """

    army_data = None

    if player.army is not None:

        army_data = {
            "faction": player.army.faction,

            "units": [
                {
                    "unit_id": army_unit.unit.id,

                    "start_position": (
                        list(army_unit.start_position)
                        if army_unit.start_position is not None
                        else None
                    ),
                }

                for army_unit in player.army.units
            ],
        }

    return {
        "player_id": player.id,

        "name": player.name,
        "faction": player.faction,
        "side": player.side,

        "army": army_data,
    }


def serialize_players(players):
    """
    Serialize all players.
    """

    return [
        serialize_player(player)
        for player in players
    ]


# ============================================================
# Unit serialization
# ============================================================

def _serialize_footprint(footprint):
    """
    Serialize a Unit Footprint.
    """

    if footprint is None:
        return None

    return {
        "width": footprint.width,
        "length": footprint.length,
    }


def serialize_unit(unit):
    """
    Serialize a live Unit into an API-safe dictionary.

    Object references such as owner are represented by IDs.
    """

    owner_id = None

    if unit.owner is not None:
        owner_id = unit.owner.id

    return {

        # ----------------------------------------------------
        # Identity
        # ----------------------------------------------------

        "unit_id": unit.id,
        "owner_id": owner_id,

        # ----------------------------------------------------
        # Definition
        # ----------------------------------------------------

        "name": unit.name,
        "faction": unit.faction,
        "rarity": unit.rarity,
        "cost": unit.cost,
        "symbol": unit.symbol,

        # ----------------------------------------------------
        # Presentation metadata
        # ----------------------------------------------------

        "fullArt_path": unit.fullArt_path,
        "icon_path": unit.icon_path,

        # ----------------------------------------------------
        # Physical characteristics
        # ----------------------------------------------------

        "footprint": _serialize_footprint(unit.footprint),

        # ----------------------------------------------------
        # Combat characteristics
        # ----------------------------------------------------

        "health": unit.health,
        "current_health": unit.current_health,

        "defense": unit.defense,
        "movement": unit.movement,
        "detection_range": unit.detection_range,

        # ----------------------------------------------------
        # Runtime state
        # ----------------------------------------------------

        "position": _serialize_position(unit.position),

        "status_effects": [
            _serialize_object(effect)
            for effect in getattr(unit, "status_effects", [])
        ],

        "cooldowns": dict(
            getattr(unit, "cooldowns", {})
        ),

        # ----------------------------------------------------
        # Equipment / capabilities
        # ----------------------------------------------------

        "attacks": [
            _serialize_object(attack)
            for attack in getattr(unit, "attacks", [])
        ],

        "abilities": [
            _serialize_object(ability)
            for ability in getattr(unit, "abilities", [])
        ],

        "passive": [
            _serialize_object(passive)
            for passive in getattr(unit, "passive", [])
        ],
    }


def serialize_units(units):
    """
    Serialize all live units.
    """

    return [
        serialize_unit(unit)
        for unit in units
    ]


# ============================================================
# Game serialization
# ============================================================

GAME_STATE_SCHEMA_VERSION = 1


def serialize_game(game):
    """
    Serialize the authoritative runtime state of a Game.

    This is the primary API-facing representation of the game.

    The returned object contains no live Python references and
    should therefore be safe to pass to JSON serialization.
    """

    map_manager = game.map_manager

    active_player_id = None

    if map_manager.active_player is not None:
        active_player_id = map_manager.active_player.id

    return {

        # ----------------------------------------------------
        # Protocol / schema metadata
        # ----------------------------------------------------

        "schema_version": GAME_STATE_SCHEMA_VERSION,

        # ----------------------------------------------------
        # Game identity / deterministic state
        # ----------------------------------------------------

        "seed": getattr(game, "seed", None),

        "turn_number": map_manager.turn_number,

        "active_player_id": active_player_id,

        "running": game.running,

        # ----------------------------------------------------
        # Map
        # ----------------------------------------------------

        "map": serialize_map(map_manager.map),

        # ----------------------------------------------------
        # Players
        # ----------------------------------------------------

        "players": serialize_players(
            map_manager.players
        ),

        # ----------------------------------------------------
        # Units
        # ----------------------------------------------------

        "units": serialize_units(
            map_manager.units
        ),
    }


def serialize_game_json(game, **json_kwargs):
    """
    Convenience helper for local development/testing.

    Returns a JSON string rather than a Python dictionary.

    The API layer should generally use serialize_game() and allow
    the web framework to perform JSON encoding.
    """

    import json

    return json.dumps(
        serialize_game(game),
        **json_kwargs
    )
