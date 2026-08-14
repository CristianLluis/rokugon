import unittest

from app.models.tiles import Edge
from app.models.tiles import Tile


class TileTestCase(unittest.TestCase):
    """
    WALL = 00
    CAVE = 01
    DUNGEON = 10
    WATER = 11
    """

    def setUp(self):
        self.tile = Tile.from_edges(Edge.WALL, Edge.CAVE, Edge.CAVE, Edge.WATER, Edge.WATER, Edge.DUNGEON)

    def test_tile_edges_can_be_read_back(self):
        # 10 11 11 01 01 00
        self.assertEqual("0b101111010100", bin(self.tile.value))
        self.assertIs(self.tile.edge(0), Edge.WALL)
        self.assertIs(self.tile.edge(1), Edge.CAVE)
        self.assertIs(self.tile.edge(2), Edge.CAVE)
        self.assertIs(self.tile.edge(3), Edge.WATER)
        self.assertIs(self.tile.edge(4), Edge.WATER)
        self.assertIs(self.tile.edge(5), Edge.DUNGEON)
