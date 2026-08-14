from enum import IntEnum


class Edge(IntEnum):
    WALL = 0b00
    CAVE = 0b01
    DUNGEON = 0b10
    WATER = 0b11


class Tile:
    def __init__(self, value: int):
        self.value = value

    @classmethod
    def from_edges(
        cls,
        edge_0: Edge,
        edge_1: Edge,
        edge_2: Edge,
        edge_3: Edge,
        edge_4: Edge,
        edge_5: Edge,
    ) -> Tile:
        value = edge_0 | edge_1 << 2 | edge_2 << 4 | edge_3 << 6 | edge_4 << 8 | edge_5 << 10

        return cls(value)

    def edge(self, index: int) -> Edge:
        value = (self.value >> (index * 2)) & 0b11
        return Edge(value)
