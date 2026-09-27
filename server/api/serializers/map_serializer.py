from enum import Enum


def serialize_feature(feature):
    """
    Serialize a TileFeature into an API-safe representation.

    Features are represented by their type and gameplay-relevant
    properties rather than by serializing the Python object.
    """

    movement_cost = feature.movement_cost()
    if movement_cost == float('inf'):
        movement_cost = None

    data = {
        "type": feature.__class__.__name__,
        "symbol": feature.symbol(),
        "tags": list(getattr(feature, "tags", set())),
        "blocks_movement": feature.blocks_movement(),
        "movement_cost": movement_cost,
    }

    # Optional gameplay properties.
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
    Serialize mape edges as connections between two cells.

    Edge endpoints are intentionally unordered pairs
    """

    edges = []

    for edge_key, edge in game_map.edges.items():
        endpoints = [
            list(position)
            for position in edge_key
        ]

        edges.append({
            "cells": endpoints, 
            "type":(
                edge.edge_type.name
                if hasattr(edge.edge_type, "name")
                else str(edge.edge_type)
            ),
            "blocks_movement": edge.blocks_movement(),
            "diagonal": edge.is_diagonal(),
        })

    return edges

def serialize_map(game_map):
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