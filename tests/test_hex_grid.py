import unittest

from app.models.hex_grid import CUBE_DIRECTIONS
from app.models.hex_grid import CubeCoordinate
from app.models.hex_grid import cube_radius
from app.models.hex_grid import opposite_edge


class HexGridTestCase(unittest.TestCase):
    def test_cube_coordinate_requires_zero_sum(self):
        with self.assertRaises(ValueError):
            CubeCoordinate(q=1, r=1, s=1)

    def test_cube_radius_counts_cells(self):
        self.assertEqual(1, len(cube_radius(0)))
        self.assertEqual(7, len(cube_radius(1)))
        self.assertEqual(19, len(cube_radius(2)))

    def test_flat_top_neighbor_order(self):
        origin = CubeCoordinate(q=0, r=0, s=0)

        self.assertEqual(CubeCoordinate(q=0, r=-1, s=1), origin.neighbor(0))
        self.assertEqual(CubeCoordinate(q=1, r=-1, s=0), origin.neighbor(1))
        self.assertEqual(CubeCoordinate(q=1, r=0, s=-1), origin.neighbor(2))
        self.assertEqual(CubeCoordinate(q=0, r=1, s=-1), origin.neighbor(3))
        self.assertEqual(CubeCoordinate(q=-1, r=1, s=0), origin.neighbor(4))
        self.assertEqual(CubeCoordinate(q=-1, r=0, s=1), origin.neighbor(5))

    def test_opposite_edges_are_three_steps_apart(self):
        for direction in range(len(CUBE_DIRECTIONS)):
            self.assertEqual(direction, opposite_edge(opposite_edge(direction)))
            self.assertEqual(3, (opposite_edge(direction) - direction) % 6)
