import unittest

from app.models.hex_grid import CubeCoordinate
from app.models.tiles import Edge
from app.services.wfc import TileVariant
from app.services.wfc import build_variants
from app.services.wfc import edges_match
from app.services.wfc import generate_map
from app.services.wfc import rotate_edges
from app.services.wfc import score_assignments
from app.services.wfc import variant_weight


class WfcTestCase(unittest.TestCase):
    def test_clockwise_rotation_moves_top_edge_to_upper_right(self):
        edges = (
            Edge.CAVE,
            Edge.WALL,
            Edge.WALL,
            Edge.WALL,
            Edge.WALL,
            Edge.WALL,
        )

        self.assertEqual(
            (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            rotate_edges(edges, 1),
        )
        self.assertEqual(edges, rotate_edges(edges, 6))

    def test_adjacent_edges_match_against_opposite_edge(self):
        left = TileVariant(
            piece_id="left",
            side="front",
            image="left.png",
            url="/assets/files/left.png",
            rotation=0,
            edges=(Edge.CAVE, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
        )
        right = TileVariant(
            piece_id="right",
            side="front",
            image="right.png",
            url="/assets/files/right.png",
            rotation=0,
            edges=(Edge.WALL, Edge.WALL, Edge.WALL, Edge.CAVE, Edge.WALL, Edge.WALL),
        )

        self.assertTrue(edges_match(left, 0, right))

    def test_physical_tile_expands_to_twelve_side_rotation_variants(self):
        physical_tile = {
            "front": {
                "image": "front.png",
                "edges": (Edge.CAVE, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
            },
            "back": {
                "image": "back.png",
                "edges": (Edge.WALL, Edge.CAVE, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
            },
        }

        variants = build_variants((("test", [physical_tile]),))

        self.assertEqual(12, len(variants))
        self.assertEqual({"test_01"}, {variant.piece_id for variant in variants})
        self.assertEqual({"front", "back"}, {variant.side for variant in variants})
        self.assertEqual(set(range(6)), {variant.rotation for variant in variants})
        self.assertEqual({2}, {variant.weight for variant in variants if variant.side == "front"})
        self.assertEqual({2}, {variant.weight for variant in variants if variant.side == "back"})

    def test_variant_weights_prefer_two_or_three_exit_tiles(self):
        self.assertEqual(2, variant_weight((Edge.CAVE, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL)))
        self.assertEqual(8, variant_weight((Edge.CAVE, Edge.WALL, Edge.WALL, Edge.CAVE, Edge.WALL, Edge.WALL)))
        self.assertEqual(6, variant_weight((Edge.CAVE, Edge.CAVE, Edge.CAVE, Edge.WALL, Edge.WALL, Edge.WALL)))
        self.assertEqual(3, variant_weight((Edge.CAVE, Edge.CAVE, Edge.CAVE, Edge.CAVE, Edge.WALL, Edge.WALL)))
        self.assertEqual(1, variant_weight((Edge.CAVE, Edge.CAVE, Edge.CAVE, Edge.CAVE, Edge.CAVE, Edge.CAVE)))
        self.assertEqual(12, variant_weight((Edge.CAVE, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL), 12))

    def test_physical_tile_can_be_used_at_most_once(self):
        physical_tile = {
            "front": {
                "image": "front.png",
                "edges": (Edge.DUNGEON, Edge.WALL, Edge.WALL, Edge.DUNGEON, Edge.WALL, Edge.WALL),
            },
            "back": {
                "image": "back.png",
                "edges": (Edge.DUNGEON, Edge.WALL, Edge.WALL, Edge.DUNGEON, Edge.WALL, Edge.WALL),
            },
        }

        generated = generate_map(
            seed=1,
            retry_limit=1,
            backtrack_limit=20,
            registries=(("test", [physical_tile]),),
        )

        self.assertEqual(1, generated.placed_count)

    def test_same_seed_generates_same_map(self):
        first = generate_map(seed=123, retry_limit=1, backtrack_limit=200)
        second = generate_map(seed=123, retry_limit=1, backtrack_limit=200)

        self.assertEqual(first, second)

    def test_map_quality_uses_exposed_dungeon_edges_for_reachability(self):
        variant = TileVariant(
            piece_id="dungeon",
            side="front",
            image="dungeon.png",
            url="/assets/files/dungeon.png",
            rotation=0,
            edges=(Edge.DUNGEON, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
        )

        center_quality = score_assignments({CubeCoordinate(q=0, r=0, s=0): 0}, (variant,), radius=1)
        boundary_quality = score_assignments({CubeCoordinate(q=0, r=-1, s=1): 0}, (variant,), radius=1)

        self.assertEqual(1, center_quality.reachable_count)
        self.assertEqual(0, center_quality.unreachable_count)
        self.assertEqual(1, boundary_quality.reachable_count)
        self.assertEqual(0, boundary_quality.unreachable_count)
        self.assertEqual(0, boundary_quality.open_edge_count)
        self.assertEqual(1, center_quality.entrance_count)

    def test_exposed_cave_counts_as_invalid_outline_edge(self):
        variant = TileVariant(
            piece_id="cave",
            side="front",
            image="cave.png",
            url="/assets/files/cave.png",
            rotation=0,
            edges=(Edge.CAVE, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
        )

        quality = score_assignments({CubeCoordinate(q=0, r=0, s=0): 0}, (variant,), radius=1)

        self.assertEqual(1, quality.invalid_outline_edge_count)
        self.assertEqual(0, quality.reachable_count)

    def test_map_quality_counts_internal_open_edges(self):
        left = TileVariant(
            piece_id="cave",
            side="front",
            image="cave.png",
            url="/assets/files/cave.png",
            rotation=2,
            edges=(Edge.WALL, Edge.WALL, Edge.CAVE, Edge.WALL, Edge.WALL, Edge.WALL),
        )
        right = TileVariant(
            piece_id="wall",
            side="front",
            image="wall.png",
            url="/assets/files/wall.png",
            rotation=0,
            edges=(Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
        )

        quality = score_assignments(
            {
                CubeCoordinate(q=0, r=0, s=0): 0,
                CubeCoordinate(q=1, r=0, s=-1): 1,
            },
            (left, right),
            radius=1,
        )

        self.assertEqual(1, quality.open_edge_count)

    def test_boundary_water_does_not_count_as_dungeon_entrance(self):
        variant = TileVariant(
            piece_id="water",
            side="front",
            image="water.png",
            url="/assets/files/water.png",
            rotation=0,
            edges=(Edge.WATER, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
        )

        quality = score_assignments({CubeCoordinate(q=0, r=-1, s=1): 0}, (variant,), radius=1)

        self.assertEqual(0, quality.reachable_count)
        self.assertEqual(0, quality.entrance_count)

    def test_map_quality_counts_unreachable_islands(self):
        variants = (
            TileVariant(
                piece_id="entrance",
                side="front",
                image="entrance.png",
                url="/assets/files/entrance.png",
                rotation=0,
                edges=(Edge.DUNGEON, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
            ),
            TileVariant(
                piece_id="island",
                side="front",
                image="island.png",
                url="/assets/files/island.png",
                rotation=0,
                edges=(Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL, Edge.WALL),
            ),
        )
        assignments = {
            CubeCoordinate(q=0, r=-1, s=1): 0,
            CubeCoordinate(q=0, r=1, s=-1): 1,
        }

        quality = score_assignments(assignments, variants, radius=1)

        self.assertEqual(1, quality.reachable_count)
        self.assertEqual(1, quality.unreachable_count)

    def test_generated_map_solves_fixed_region_from_reachable_entrance(self):
        physical_tiles = [
            {
                "front": {
                    "image": f"front_{index}.png",
                    "edges": (Edge.DUNGEON, Edge.WALL, Edge.WALL, Edge.DUNGEON, Edge.WALL, Edge.WALL),
                },
                "back": {
                    "image": f"back_{index}.png",
                    "edges": (Edge.DUNGEON, Edge.WALL, Edge.WALL, Edge.DUNGEON, Edge.WALL, Edge.WALL),
                },
            }
            for index in range(3)
        ]

        generated = generate_map(
            seed=10,
            retry_limit=1,
            backtrack_limit=50,
            registries=(("test", physical_tiles),),
        )
        variants_by_url_and_rotation = {
            (variant.url, variant.rotation): variant for variant in build_variants((("test", physical_tiles),))
        }
        assignments = {
            CubeCoordinate(q=placement.q, r=placement.r, s=placement.s): variant_index
            for variant_index, placement in enumerate(generated.placements)
        }
        placement_variants = tuple(
            variants_by_url_and_rotation[(placement.url, placement.rotation)] for placement in generated.placements
        )
        quality = score_assignments(assignments, placement_variants, radius=generated.radius)

        self.assertEqual(generated.placed_count, quality.reachable_count)
        self.assertEqual(0, quality.unreachable_count)

    def test_generation_uses_exactly_two_dungeon_outline_openings(self):
        physical_tiles = [
            {
                "front": {
                    "image": "front.png",
                    "edges": (Edge.DUNGEON, Edge.WALL, Edge.WALL, Edge.DUNGEON, Edge.WALL, Edge.WALL),
                },
                "back": {
                    "image": "back.png",
                    "edges": (Edge.DUNGEON, Edge.WALL, Edge.WALL, Edge.DUNGEON, Edge.WALL, Edge.WALL),
                },
            }
        ]

        generated = generate_map(
            seed=1,
            retry_limit=1,
            backtrack_limit=20,
            registries=(("test", physical_tiles),),
        )
        radius = generated.radius
        variants_by_url_and_rotation = {
            (variant.url, variant.rotation): variant for variant in build_variants((("test", physical_tiles),))
        }
        dungeon_outline_edge_count = 0

        for placement in generated.placements:
            coordinate = CubeCoordinate(q=placement.q, r=placement.r, s=placement.s)
            variant = variants_by_url_and_rotation[(placement.url, placement.rotation)]
            for direction, edge in enumerate(variant.edges):
                if edge != Edge.DUNGEON:
                    continue

                neighbor = coordinate.neighbor(direction)
                if max(abs(neighbor.q), abs(neighbor.r), abs(neighbor.s)) > radius:
                    dungeon_outline_edge_count += 1

        self.assertEqual(2, dungeon_outline_edge_count)

    def test_generated_map_has_exactly_two_entrances(self):
        generated = generate_map(seed=12, retry_limit=1, backtrack_limit=1000)
        variants = build_variants()
        variants_by_url_and_rotation = {
            (variant.url, variant.rotation): variant_index for variant_index, variant in enumerate(variants)
        }
        assignments = {
            CubeCoordinate(q=placement.q, r=placement.r, s=placement.s): variants_by_url_and_rotation[
                (placement.url, placement.rotation)
            ]
            for placement in generated.placements
        }
        quality = score_assignments(assignments, variants, radius=generated.radius)

        self.assertEqual(2, quality.entrance_count)
        self.assertEqual(0, quality.invalid_outline_edge_count)
        self.assertEqual(generated.placed_count, quality.reachable_count)

    def test_generated_map_caps_dungeon_outer_edges_and_rejects_cave_outer_edges(self):
        generated = generate_map(seed=22, retry_limit=1, backtrack_limit=1000)
        radius = generated.radius
        variants = build_variants()
        variants_by_url_and_rotation = {
            (variant.url, variant.rotation): variant for variant in variants
        }
        assigned_cells = {
            CubeCoordinate(q=placement.q, r=placement.r, s=placement.s)
            for placement in generated.placements
        }
        cave_outer_edge_count = 0
        dungeon_outer_edge_count = 0

        for placement in generated.placements:
            coordinate = CubeCoordinate(q=placement.q, r=placement.r, s=placement.s)
            variant = variants_by_url_and_rotation[(placement.url, placement.rotation)]

            for direction, edge in enumerate(variant.edges):
                neighbor = coordinate.neighbor(direction)
                if (
                    neighbor in assigned_cells
                    and max(abs(neighbor.q), abs(neighbor.r), abs(neighbor.s)) <= radius
                ):
                    continue
                if edge == Edge.CAVE:
                    cave_outer_edge_count += 1
                if edge == Edge.DUNGEON:
                    dungeon_outer_edge_count += 1

        self.assertEqual(0, cave_outer_edge_count)
        self.assertEqual(2, dungeon_outer_edge_count)
