import heapq, math

class MovementManager:
    DIRECTIONS = (
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    )

    def __init__(self, map_manager):
        self.map_manager = map_manager

    def get_reachable_tiles(self, unit):
        start = unit.position
        max_cost = unit.movement

        distances = {start: 0}

        queue = [(0, start)]

        while queue:
            current_cost, current = heapq.heappop(queue)
            if current_cost > distances[current]:
                continue

            for neighbor in self.get_neighbors(current):
                if not self.can_enter(unit, neighbor):
                    continue

                tile_cost = self.get_tile_cost(neighbor)

                new_cost = current_cost + tile_cost

                if new_cost > max_cost:
                    continue

                if (
                    neighbor not in distances
                    or new_cost < distances[neighbor]
                ):
                    distances[neighbor] = new_cost

                    heapq.heappush(
                        queue,
                        (new_cost, neighbor)
                    )

        return set(distances.keys())


    def get_neighbors(self, position):
        x, y = position

        for dx, dy in self.DIRECTIONS:
            neighbor = (x + dx, y + dy)

            if self.map_manager.in_bounds(neighbor):
                yield neighbor

    def get_tile_cost(self, position):
        tile = self.map_manager.get_tile(position)
        return tile.movement_cost()

    def can_enter(self, unit, position):
        tile = self.map_manager.get_tile(position)
        if tile.blocks_movement():
            return False
        return self.map_manager.can_place(position, unitToPlace=unit)