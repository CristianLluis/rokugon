from collections.abc import Mapping
from collections.abc import Sequence
from dataclasses import dataclass
from math import atan2
from random import Random
from random import SystemRandom

from app.assets.caverns import CAVERN_TERRAIN
from app.assets.dungeons import DUNGEON_TERRAIN
from app.assets.other import OTHER_TERRAIN
from app.assets.rivers import RIVERS_TERRAIN
from app.models.hex_grid import CubeCoordinate
from app.models.hex_grid import cube_radius
from app.models.hex_grid import opposite_edge
from app.models.tiles import Edge


ASSET_URL_PREFIX = "/assets/files"
DEFAULT_RETRY_LIMIT = 1
DEFAULT_BACKTRACK_LIMIT = 300
MAX_VARIANT_BRANCHES = 48
MAX_ENTRANCE_COUNT = 2
TRAVERSABLE_EDGES = frozenset((Edge.CAVE, Edge.DUNGEON, Edge.WATER))
ENTRANCE_EDGES = frozenset((Edge.DUNGEON,))
OUTER_EDGE_EDGES = frozenset((Edge.WALL, Edge.DUNGEON, Edge.WATER))
NON_ENTRANCE_OUTER_EDGE_EDGES = frozenset((Edge.WALL, Edge.WATER))

TerrainSide = Mapping[str, object]
PhysicalTile = Mapping[str, TerrainSide]
TerrainRegistry = tuple[str, Sequence[PhysicalTile]]

TERRAIN_REGISTRIES: tuple[TerrainRegistry, ...] = (
    ("caverns", CAVERN_TERRAIN),
    ("dungeons", DUNGEON_TERRAIN),
    ("other", OTHER_TERRAIN),
    ("rivers", RIVERS_TERRAIN),
)


@dataclass(frozen=True, slots=True)
class TileVariant:
    piece_id: str
    side: str
    image: str
    url: str
    rotation: int
    edges: tuple[Edge, Edge, Edge, Edge, Edge, Edge]
    weight: int = 1


@dataclass(frozen=True, slots=True)
class Placement:
    url: str
    title: str
    q: int
    r: int
    s: int
    rotation: int


@dataclass(frozen=True, slots=True)
class GeneratedMap:
    placements: tuple[Placement, ...]
    seed: int
    radius: int

    @property
    def placed_count(self) -> int:
        return len(self.placements)


@dataclass(frozen=True, slots=True)
class MapQuality:
    reachable_count: int
    unreachable_count: int
    invalid_outline_edge_count: int
    open_edge_count: int
    dead_end_count: int
    entrance_count: int
    placed_count: int

    def score(self) -> tuple[int, int, int, int, int, int, int, int]:
        entrance_excess = max(0, self.entrance_count - MAX_ENTRANCE_COUNT)
        entrance_gap = abs(MAX_ENTRANCE_COUNT - self.entrance_count)

        return (
            -self.invalid_outline_edge_count,
            -entrance_excess,
            -entrance_gap,
            self.reachable_count,
            -self.unreachable_count,
            -self.open_edge_count,
            -self.dead_end_count,
            self.placed_count,
        )


def rotate_edges(edges: Sequence[Edge], rotation: int) -> tuple[Edge, Edge, Edge, Edge, Edge, Edge]:
    if len(edges) != 6:
        raise ValueError("hex tiles must define exactly 6 edges")

    rotated = [Edge.WALL] * 6
    for index, edge in enumerate(edges):
        rotated[(index + rotation) % 6] = edge

    return (
        rotated[0],
        rotated[1],
        rotated[2],
        rotated[3],
        rotated[4],
        rotated[5],
    )


def edges_match(left: TileVariant, direction: int, right: TileVariant) -> bool:
    return left.edges[direction] == right.edges[opposite_edge(direction)]


def edge_is_traversable(edge: Edge) -> bool:
    return edge in TRAVERSABLE_EDGES


def edge_is_entrance(edge: Edge) -> bool:
    return edge in ENTRANCE_EDGES


def variant_weight(edges: Sequence[Edge], explicit_weight: object = None) -> int:
    if explicit_weight is not None:
        return max(1, int(explicit_weight))

    traversable_count = sum(1 for edge in edges if edge_is_traversable(edge))
    if traversable_count == 0:
        return 1
    if traversable_count == 1:
        return 2
    if traversable_count == 2:
        return 8
    if traversable_count == 3:
        return 6
    if traversable_count == 4:
        return 3

    return 1


def build_variants(registries: Sequence[TerrainRegistry] = TERRAIN_REGISTRIES) -> tuple[TileVariant, ...]:
    variants = []
    for registry_name, physical_tiles in registries:
        for piece_number, physical_tile in enumerate(physical_tiles, start=1):
            piece_id = f"{registry_name}_{piece_number:02d}"
            for side in ("front", "back"):
                side_config = physical_tile[side]
                image = side_config["image"]
                edges = side_config["edges"]
                weight = variant_weight(edges, side_config.get("weight"))

                if not isinstance(image, str):
                    raise TypeError("tile image must be a string")

                for rotation in range(6):
                    variants.append(
                        TileVariant(
                            piece_id=piece_id,
                            side=side,
                            image=image,
                            url=f"{ASSET_URL_PREFIX}/{image}",
                            rotation=rotation,
                            edges=rotate_edges(edges, rotation),
                            weight=weight,
                        )
                    )

    return tuple(variants)


def generate_map(
    *,
    seed: int | None = None,
    retry_limit: int = DEFAULT_RETRY_LIMIT,
    backtrack_limit: int = DEFAULT_BACKTRACK_LIMIT,
    registries: Sequence[TerrainRegistry] = TERRAIN_REGISTRIES,
) -> GeneratedMap:
    if retry_limit < 1:
        raise ValueError("retry_limit must be greater than or equal to 1")
    if backtrack_limit < 0:
        raise ValueError("backtrack_limit must be greater than or equal to 0")

    resolved_seed = seed if seed is not None else SystemRandom().randrange(2**63)
    variants = build_variants(registries)
    piece_count = len({variant.piece_id for variant in variants})
    radius = _radius_for_cell_count(piece_count)
    cells = _compact_cell_region(cube_radius(radius), piece_count)
    target_count = piece_count

    if not cells or not variants or target_count == 0:
        return GeneratedMap(placements=(), seed=resolved_seed, radius=radius)

    seed_rng = Random(resolved_seed)
    best_assignments: dict[CubeCoordinate, int] = {}
    best_quality = MapQuality(
        reachable_count=0,
        unreachable_count=0,
        invalid_outline_edge_count=0,
        open_edge_count=0,
        dead_end_count=0,
        entrance_count=0,
        placed_count=0,
    )

    for _ in range(retry_limit):
        attempt_rng = Random(seed_rng.randrange(2**63))
        solver = _Solver(cells, variants, target_count, radius, attempt_rng, backtrack_limit)
        assignments = solver.solve()
        quality = score_assignments(assignments, variants, radius)

        if quality.score() > best_quality.score():
            best_assignments = assignments
            best_quality = quality

        if (
            best_quality.reachable_count >= target_count
            and best_quality.invalid_outline_edge_count == 0
            and best_quality.entrance_count == MAX_ENTRANCE_COUNT
            and best_quality.open_edge_count == 0
            and best_quality.dead_end_count == 0
        ):
            break

    placements = tuple(
        Placement(
            url=variants[variant_id].url,
            title=variants[variant_id].image,
            q=coordinate.q,
            r=coordinate.r,
            s=coordinate.s,
            rotation=variants[variant_id].rotation,
        )
        for coordinate, variant_id in sorted(best_assignments.items())
    )

    return GeneratedMap(placements=placements, seed=resolved_seed, radius=radius)


def _radius_for_cell_count(cell_count: int) -> int:
    radius = 0
    while 1 + 3 * radius * (radius + 1) < cell_count:
        radius += 1

    return radius


def _compact_cell_region(
    cells: Sequence[CubeCoordinate],
    target_count: int,
) -> tuple[CubeCoordinate, ...]:
    if target_count >= len(cells):
        return tuple(sorted(cells))

    radius = 0
    while 1 + 3 * radius * (radius + 1) < target_count:
        radius += 1

    inner_cells = [
        cell
        for cell in cells
        if max(abs(cell.q), abs(cell.r), abs(cell.s)) < radius
    ]
    outer_cells = [
        cell
        for cell in cells
        if max(abs(cell.q), abs(cell.r), abs(cell.s)) == radius
    ]
    outer_cells.sort(key=_cell_angle)
    outer_count = target_count - len(inner_cells)

    if outer_count >= len(outer_cells):
        return tuple(sorted([*inner_cells, *outer_cells]))

    selected_outer_cells = []
    used_indexes: set[int] = set()
    for index in range(outer_count):
        selected_index = round(index * len(outer_cells) / outer_count) % len(outer_cells)
        while selected_index in used_indexes:
            selected_index = (selected_index + 1) % len(outer_cells)
        used_indexes.add(selected_index)
        selected_outer_cells.append(outer_cells[selected_index])

    return tuple(sorted([*inner_cells, *selected_outer_cells]))


def _cell_angle(cell: CubeCoordinate) -> float:
    return atan2(_print_layer(cell), 3 * cell.q)


def _print_layer(cell: CubeCoordinate) -> int:
    return 2 * cell.r + cell.q


def score_assignments(
    assignments: Mapping[CubeCoordinate, int],
    variants: Sequence[TileVariant],
    radius: int,
) -> MapQuality:
    reachable_cells = _reachable_cells(assignments, variants, radius)
    invalid_outline_edge_count = _invalid_outline_edge_count(assignments, variants, radius)
    open_edge_count = _open_internal_edge_count(assignments, variants, radius)
    dead_end_count = _dead_end_count(assignments, variants, radius, reachable_cells)
    entrance_count = _entrance_count(assignments, variants, radius)
    placed_count = len(assignments)

    return MapQuality(
        reachable_count=len(reachable_cells),
        unreachable_count=placed_count - len(reachable_cells),
        invalid_outline_edge_count=invalid_outline_edge_count,
        open_edge_count=open_edge_count,
        dead_end_count=dead_end_count,
        entrance_count=entrance_count,
        placed_count=placed_count,
    )


def _reachable_cells(
    assignments: Mapping[CubeCoordinate, int],
    variants: Sequence[TileVariant],
    radius: int,
) -> set[CubeCoordinate]:
    entrance_cells = [
        coordinate
        for coordinate, variant_id in assignments.items()
        if _has_exposed_entrance_edge(coordinate, variants[variant_id], assignments, radius)
    ]
    reachable = set(entrance_cells)
    queue = list(entrance_cells)

    while queue:
        coordinate = queue.pop()
        variant = variants[assignments[coordinate]]

        for direction in range(6):
            neighbor = coordinate.neighbor(direction)
            neighbor_variant_id = assignments.get(neighbor)
            if neighbor_variant_id is None:
                continue

            if not _variants_connect(variant, direction, variants[neighbor_variant_id]):
                continue

            if neighbor not in reachable:
                reachable.add(neighbor)
                queue.append(neighbor)

    return reachable


def _edge_is_exposed(
    coordinate: CubeCoordinate,
    direction: int,
    assignments: Mapping[CubeCoordinate, int],
    radius: int,
) -> bool:
    neighbor = coordinate.neighbor(direction)

    return neighbor not in assignments or _is_outside_radius(neighbor, radius)


def _has_exposed_entrance_edge(
    coordinate: CubeCoordinate,
    variant: TileVariant,
    assignments: Mapping[CubeCoordinate, int],
    radius: int,
) -> bool:
    return any(
        _edge_is_exposed(coordinate, direction, assignments, radius) and edge_is_entrance(edge)
        for direction in range(6)
        for edge in (variant.edges[direction],)
    )


def _entrance_count(
    assignments: Mapping[CubeCoordinate, int],
    variants: Sequence[TileVariant],
    radius: int,
) -> int:
    return sum(
        1
        for coordinate, variant_id in assignments.items()
        for direction, edge in enumerate(variants[variant_id].edges)
        if edge_is_entrance(edge) and _edge_is_exposed(coordinate, direction, assignments, radius)
    )


def _dead_end_count(
    assignments: Mapping[CubeCoordinate, int],
    variants: Sequence[TileVariant],
    radius: int,
    reachable_cells: set[CubeCoordinate],
) -> int:
    return sum(1 for coordinate in reachable_cells if _is_dead_end(coordinate, assignments, variants, radius))


def _invalid_outline_edge_count(
    assignments: Mapping[CubeCoordinate, int],
    variants: Sequence[TileVariant],
    radius: int,
) -> int:
    return sum(
        1
        for coordinate, variant_id in assignments.items()
        for direction, edge in enumerate(variants[variant_id].edges)
        if edge not in OUTER_EDGE_EDGES and _edge_is_exposed(coordinate, direction, assignments, radius)
    )


def _open_internal_edge_count(
    assignments: Mapping[CubeCoordinate, int],
    variants: Sequence[TileVariant],
    radius: int,
) -> int:
    open_edge_count = 0

    for coordinate, variant_id in assignments.items():
        variant = variants[variant_id]
        for direction, edge in enumerate(variant.edges):
            if not edge_is_traversable(edge):
                continue

            neighbor = coordinate.neighbor(direction)
            if _is_outside_radius(neighbor, radius) or neighbor not in assignments:
                continue

            neighbor_variant_id = assignments[neighbor]
            if not _variants_connect(variant, direction, variants[neighbor_variant_id]):
                open_edge_count += 1

    return open_edge_count


def _is_dead_end(
    coordinate: CubeCoordinate,
    assignments: Mapping[CubeCoordinate, int],
    variants: Sequence[TileVariant],
    radius: int,
) -> bool:
    return _traversable_degree(coordinate, assignments, variants, radius) <= 1


def _traversable_degree(
    coordinate: CubeCoordinate,
    assignments: Mapping[CubeCoordinate, int],
    variants: Sequence[TileVariant],
    radius: int,
) -> int:
    variant = variants[assignments[coordinate]]
    degree = 0

    for direction in range(6):
        neighbor = coordinate.neighbor(direction)
        neighbor_variant_id = assignments.get(neighbor)

        if neighbor_variant_id is not None:
            if _variants_connect(variant, direction, variants[neighbor_variant_id]):
                degree += 1
            continue

        if neighbor_variant_id is None and edge_is_traversable(variant.edges[direction]):
            degree += 1

    return degree


def _is_outside_radius(coordinate: CubeCoordinate, radius: int) -> bool:
    return max(abs(coordinate.q), abs(coordinate.r), abs(coordinate.s)) > radius


def _variants_connect(left: TileVariant, direction: int, right: TileVariant) -> bool:
    return edge_is_traversable(left.edges[direction]) and edges_match(left, direction, right)


class _Solver:
    def __init__(
        self,
        cells: Sequence[CubeCoordinate],
        variants: Sequence[TileVariant],
        target_count: int,
        radius: int,
        rng: Random,
        backtrack_limit: int,
    ):
        self.cells = tuple(cells)
        self.cell_set = set(cells)
        self.variants = tuple(variants)
        self.target_count = target_count
        self.radius = radius
        self.rng = rng
        self.backtrack_limit = backtrack_limit
        self.backtrack_count = 0
        self.best_assignments: dict[CubeCoordinate, int] = {}
        self.best_search_score: tuple[int, int, int, int, int] = (
            -1,
            -MAX_ENTRANCE_COUNT - 1,
            -MAX_ENTRANCE_COUNT,
            0,
            0,
        )
        self.neighbor_slots = {
            cell: tuple(
                neighbor if (neighbor := cell.neighbor(direction)) in self.cell_set else None
                for direction in range(6)
            )
            for cell in self.cells
        }
        self.neighbors: dict[CubeCoordinate, tuple[tuple[int, CubeCoordinate], ...]] = {
            cell: tuple(
                (direction, neighbor)
                for direction, neighbor in enumerate(self.neighbor_slots[cell])
                if neighbor is not None
            )
            for cell in self.cells
        }
        self.cell_outside_masks = self._build_cell_outside_masks()
        self.cell_opening_masks = self._build_cell_opening_masks()
        self.variant_bits = tuple(1 << variant_id for variant_id in range(len(self.variants)))
        self.all_variant_mask = (1 << len(self.variants)) - 1
        self.variant_traversable_masks = self._build_variant_traversable_masks()
        self.variant_entrance_masks = self._build_variant_entrance_masks()
        self.variant_invalid_outline_masks = self._build_variant_invalid_outline_masks()
        self.variant_non_entrance_outer_invalid_masks = (
            self._build_variant_non_entrance_outer_invalid_masks()
        )
        self.same_piece_masks = self._build_same_piece_masks()
        self.compatible_masks_by_variant_direction = self._build_compatible_masks_by_variant_direction()
        self.initial_domains = self._build_initial_domains()

    def solve(self) -> dict[CubeCoordinate, int]:
        domains = self.initial_domains.copy()
        self._search(domains, {})

        return self.best_assignments

    def _build_cell_outside_masks(self) -> dict[CubeCoordinate, int]:
        outside_masks = {}
        for cell in self.cells:
            mask = 0
            for direction, neighbor in enumerate(self.neighbor_slots[cell]):
                if neighbor is None:
                    mask |= 1 << direction
            outside_masks[cell] = mask

        return outside_masks

    def _build_cell_opening_masks(self) -> dict[CubeCoordinate, int]:
        opening_edges = self._select_opening_edges()
        opening_masks = {cell: 0 for cell in self.cells}

        for cell, direction in opening_edges:
            opening_masks[cell] |= 1 << direction

        return opening_masks

    def _select_opening_edges(self) -> tuple[tuple[CubeCoordinate, int], ...]:
        boundary_edges = [
            (cell, direction)
            for cell in self.cells
            for direction, neighbor in enumerate(self.neighbor_slots[cell])
            if neighbor is None
        ]
        if len(boundary_edges) <= MAX_ENTRANCE_COUNT:
            return tuple(boundary_edges)

        entrance = max(
            boundary_edges,
            key=lambda item: (
                _print_layer(item[0]),
                item[1] == 3,
                -abs(item[0].q),
                -abs(item[0].r),
            ),
        )
        exit_edge = min(
            (item for item in boundary_edges if item != entrance),
            key=lambda item: (
                _print_layer(item[0]),
                item[1] != 0,
                abs(item[0].q),
                abs(item[0].r),
            ),
        )

        return entrance, exit_edge

    def _build_variant_traversable_masks(self) -> tuple[int, ...]:
        traversable_masks = []
        for variant in self.variants:
            mask = 0
            for direction, edge in enumerate(variant.edges):
                if edge_is_traversable(edge):
                    mask |= 1 << direction
            traversable_masks.append(mask)

        return tuple(traversable_masks)

    def _build_variant_entrance_masks(self) -> tuple[int, ...]:
        entrance_masks = []
        for variant in self.variants:
            mask = 0
            for direction, edge in enumerate(variant.edges):
                if edge_is_entrance(edge):
                    mask |= 1 << direction
            entrance_masks.append(mask)

        return tuple(entrance_masks)

    def _build_variant_invalid_outline_masks(self) -> tuple[int, ...]:
        invalid_outline_masks = []
        for variant in self.variants:
            mask = 0
            for direction, edge in enumerate(variant.edges):
                if edge not in OUTER_EDGE_EDGES:
                    mask |= 1 << direction
            invalid_outline_masks.append(mask)

        return tuple(invalid_outline_masks)

    def _build_variant_non_entrance_outer_invalid_masks(self) -> tuple[int, ...]:
        outer_invalid_masks = []
        for variant in self.variants:
            mask = 0
            for direction, edge in enumerate(variant.edges):
                if edge not in NON_ENTRANCE_OUTER_EDGE_EDGES:
                    mask |= 1 << direction
            outer_invalid_masks.append(mask)

        return tuple(outer_invalid_masks)

    def _build_same_piece_masks(self) -> tuple[int, ...]:
        piece_masks: dict[str, int] = {}
        for variant_id, variant in enumerate(self.variants):
            piece_masks[variant.piece_id] = piece_masks.get(variant.piece_id, 0) | self.variant_bits[variant_id]

        return tuple(piece_masks[variant.piece_id] for variant in self.variants)

    def _build_compatible_masks_by_variant_direction(self) -> tuple[tuple[int, ...], ...]:
        edge_masks_by_direction: list[dict[Edge, int]] = []
        for direction in range(6):
            opposite = opposite_edge(direction)
            edge_masks = {edge: 0 for edge in Edge}
            for variant_id, variant in enumerate(self.variants):
                edge_masks[variant.edges[opposite]] |= self.variant_bits[variant_id]
            edge_masks_by_direction.append(edge_masks)

        compatible_masks_by_variant_direction = []
        for variant in self.variants:
            compatible_masks_by_variant_direction.append(
                tuple(
                    edge_masks_by_direction[direction][variant.edges[direction]]
                    for direction in range(6)
                )
            )

        return tuple(compatible_masks_by_variant_direction)

    def _build_initial_domains(self) -> dict[CubeCoordinate, int]:
        domains = {}
        for cell in self.cells:
            outside_mask = self.cell_outside_masks[cell]
            opening_mask = self.cell_opening_masks[cell]
            non_opening_mask = outside_mask & ~opening_mask
            domain = self.all_variant_mask

            for variant_id, variant_entrance_mask in enumerate(self.variant_entrance_masks):
                if opening_mask & ~variant_entrance_mask:
                    domain &= ~self.variant_bits[variant_id]

            for variant_id, invalid_mask in enumerate(self.variant_non_entrance_outer_invalid_masks):
                if non_opening_mask & invalid_mask:
                    domain &= ~self.variant_bits[variant_id]

            domains[cell] = domain

        return domains

    def _search(self, domains: dict[CubeCoordinate, int], assignments: dict[CubeCoordinate, int]) -> bool:
        invalid_outline_edge_count = self._invalid_outline_edge_count(assignments)
        entrance_count = self._entrance_count(assignments)
        entrance_excess = max(0, entrance_count - MAX_ENTRANCE_COUNT)
        entrance_gap = abs(MAX_ENTRANCE_COUNT - entrance_count)
        search_score = (
            -invalid_outline_edge_count,
            -entrance_excess,
            -entrance_gap,
            len(assignments),
            -self._open_internal_edge_count(assignments),
        )
        if search_score > self.best_search_score:
            self.best_assignments = assignments.copy()
            self.best_search_score = search_score

        if len(assignments) >= self.target_count:
            return (
                self._invalid_outline_edge_count(assignments) == 0
                and self._entrance_count(assignments) == MAX_ENTRANCE_COUNT
                and self._open_internal_edge_count(assignments) == 0
            )

        if self.backtrack_count >= self.backtrack_limit:
            return False

        candidates = self._candidate_cells(domains, assignments)
        if not candidates:
            return False

        cell = self._choose_cell(candidates, domains, assignments)
        choices = self._ranked_variant_choices(
            cell, self._candidate_variants(cell, domains[cell], assignments), assignments
        )

        for variant_id in choices:
            if self.backtrack_count >= self.backtrack_limit:
                break

            next_domains = domains.copy()
            next_assignments = assignments.copy()

            if self._assign(next_domains, next_assignments, cell, variant_id):
                if self._search(next_domains, next_assignments):
                    return True
                self.backtrack_count += 1
            else:
                self.backtrack_count += 1

        return False

    def _choose_cell(
        self,
        candidates: Sequence[CubeCoordinate],
        domains: dict[CubeCoordinate, int],
        assignments: dict[CubeCoordinate, int],
    ) -> CubeCoordinate:
        scored_cells = []
        for cell in candidates:
            variant_mask = self._candidate_variants(cell, domains[cell], assignments)
            score = max(
                self._placement_score(cell, variant_id, assignments)
                for variant_id in self._iter_mask(variant_mask)
            )
            scored_cells.append((score, variant_mask.bit_count(), cell))

        best_entropy = min(entropy for _, entropy, _ in scored_cells)
        best_score = max(score for score, entropy, _ in scored_cells if entropy == best_entropy)
        best_cells = [cell for score, entropy, cell in scored_cells if score == best_score and entropy == best_entropy]

        return self.rng.choice(best_cells)

    def _ranked_variant_choices(
        self,
        cell: CubeCoordinate,
        variant_mask: int,
        assignments: dict[CubeCoordinate, int],
    ) -> list[int]:
        choices_by_score: dict[int, list[int]] = {}
        for variant_id in self._iter_mask(variant_mask):
            score = self._placement_score(cell, variant_id, assignments)
            choices_by_score.setdefault(score, []).append(variant_id)

        choices = []
        for score in sorted(choices_by_score, reverse=True):
            remaining_branch_count = MAX_VARIANT_BRANCHES - len(choices)
            if remaining_branch_count <= 0:
                break
            choices.extend(self._weighted_variant_order(choices_by_score[score], remaining_branch_count))

        return choices

    def _weighted_variant_order(self, variant_ids: Sequence[int], limit: int) -> list[int]:
        remaining = list(variant_ids)
        ordered = []

        while remaining and len(ordered) < limit:
            total_weight = sum(self.variants[variant_id].weight for variant_id in remaining)
            target = self.rng.uniform(0, total_weight)
            upto = 0

            for index, variant_id in enumerate(remaining):
                upto += self.variants[variant_id].weight
                if upto >= target:
                    ordered.append(variant_id)
                    remaining.pop(index)
                    break

        return ordered

    def _placement_score(
        self,
        cell: CubeCoordinate,
        variant_id: int,
        assignments: dict[CubeCoordinate, int],
    ) -> int:
        connection_count = self._assignment_connection_count(cell, variant_id, assignments)
        future_exit_count = self._future_exit_count(cell, variant_id, assignments)
        entrance_penalty = 0
        if assignments:
            entrance_count = self._entrance_count(assignments)
            next_entrance_count = self._entrance_count_after_assignment(
                cell,
                variant_id,
                assignments,
                entrance_count,
            )
            invalid_outline_count = self._invalid_outline_count_after_assignment(
                cell,
                variant_id,
                assignments,
                self._invalid_outline_edge_count(assignments),
            )
            entrance_penalty = (
                invalid_outline_count * 30
                + abs(MAX_ENTRANCE_COUNT - next_entrance_count) * 4
                + max(0, next_entrance_count - MAX_ENTRANCE_COUNT) * 20
            )
        dead_end_penalty = 5 if connection_count + future_exit_count <= 1 else 0

        return connection_count * 8 + future_exit_count * 3 - entrance_penalty - dead_end_penalty

    def _candidate_cells(
        self,
        domains: dict[CubeCoordinate, int],
        assignments: dict[CubeCoordinate, int],
    ) -> list[CubeCoordinate]:
        return [
            cell
            for cell in self.cells
            if cell not in assignments
            and domains[cell]
            and self._candidate_variants(cell, domains[cell], assignments)
        ]

    def _candidate_variants(
        self,
        cell: CubeCoordinate,
        variant_mask: int,
        assignments: dict[CubeCoordinate, int],
    ) -> int:
        return variant_mask

    def _entrance_count(self, assignments: dict[CubeCoordinate, int]) -> int:
        return sum(
            self._entrance_edge_count(cell, variant_id, assignments)
            for cell, variant_id in assignments.items()
        )

    def _entrance_edge_count(
        self,
        cell: CubeCoordinate,
        variant_id: int,
        assignments: dict[CubeCoordinate, int],
    ) -> int:
        entrance_count = 0

        for direction in self._iter_direction_mask(self.variant_entrance_masks[variant_id]):
            neighbor = self.neighbor_slots[cell][direction]
            if neighbor is None or neighbor not in assignments:
                entrance_count += 1

        return entrance_count

    def _entrance_count_after_assignment(
        self,
        cell: CubeCoordinate,
        variant_id: int,
        assignments: dict[CubeCoordinate, int],
        entrance_count: int,
    ) -> int:
        next_entrance_count = entrance_count

        for direction in self._iter_direction_mask(self.variant_entrance_masks[variant_id]):
            neighbor = self.neighbor_slots[cell][direction]
            if neighbor is None or neighbor not in assignments:
                next_entrance_count += 1

        for direction, neighbor in enumerate(self.neighbor_slots[cell]):
            if neighbor is None or neighbor not in assignments:
                continue

            neighbor_variant_id = assignments[neighbor]
            neighbor_direction = opposite_edge(direction)
            neighbor_entrance_mask = self.variant_entrance_masks[neighbor_variant_id]
            if neighbor_entrance_mask & (1 << neighbor_direction):
                next_entrance_count -= 1

        return next_entrance_count

    def _invalid_outline_edge_count(self, assignments: dict[CubeCoordinate, int]) -> int:
        return sum(
            self._invalid_outline_edge_count_for_cell(cell, variant_id, assignments)
            for cell, variant_id in assignments.items()
        )

    def _invalid_outline_edge_count_for_cell(
        self,
        cell: CubeCoordinate,
        variant_id: int,
        assignments: dict[CubeCoordinate, int],
    ) -> int:
        invalid_outline_count = 0

        for direction in self._iter_direction_mask(self.variant_invalid_outline_masks[variant_id]):
            neighbor = self.neighbor_slots[cell][direction]
            if neighbor is None or neighbor not in assignments:
                invalid_outline_count += 1

        return invalid_outline_count

    def _invalid_outline_count_after_assignment(
        self,
        cell: CubeCoordinate,
        variant_id: int,
        assignments: dict[CubeCoordinate, int],
        invalid_outline_count: int,
    ) -> int:
        next_invalid_outline_count = invalid_outline_count

        for direction in self._iter_direction_mask(self.variant_invalid_outline_masks[variant_id]):
            neighbor = self.neighbor_slots[cell][direction]
            if neighbor is None or neighbor not in assignments:
                next_invalid_outline_count += 1

        for direction, neighbor in enumerate(self.neighbor_slots[cell]):
            if neighbor is None or neighbor not in assignments:
                continue

            neighbor_variant_id = assignments[neighbor]
            neighbor_direction = opposite_edge(direction)
            neighbor_invalid_outline_mask = self.variant_invalid_outline_masks[neighbor_variant_id]
            if neighbor_invalid_outline_mask & (1 << neighbor_direction):
                next_invalid_outline_count -= 1

        return next_invalid_outline_count

    def _open_internal_edge_count(self, assignments: dict[CubeCoordinate, int]) -> int:
        open_edge_count = 0

        for cell, variant_id in assignments.items():
            traversable_mask = self.variant_traversable_masks[variant_id]
            internal_open_mask = traversable_mask & ~self.cell_outside_masks[cell]

            for direction in self._iter_direction_mask(internal_open_mask):
                neighbor = self.neighbor_slots[cell][direction]
                if neighbor is None or neighbor not in assignments:
                    continue

                neighbor_variant_id = assignments[neighbor]
                if not self._variants_connect_by_id(variant_id, direction, neighbor_variant_id):
                    open_edge_count += 1

        return open_edge_count

    def _assignment_connection_count(
        self,
        cell: CubeCoordinate,
        variant_id: int,
        assignments: dict[CubeCoordinate, int],
    ) -> int:
        return sum(
            1
            for direction, neighbor in enumerate(self.neighbor_slots[cell])
            if neighbor is not None
            and neighbor in assignments
            and self._variants_connect_by_id(variant_id, direction, assignments[neighbor])
        )

    def _future_exit_count(
        self,
        cell: CubeCoordinate,
        variant_id: int,
        assignments: dict[CubeCoordinate, int],
    ) -> int:
        variant = self.variants[variant_id]

        return sum(
            1
            for direction, neighbor in enumerate(self.neighbor_slots[cell])
            if neighbor is not None
            and neighbor not in assignments
            and edge_is_traversable(variant.edges[direction])
        )

    def _assign(
        self,
        domains: dict[CubeCoordinate, int],
        assignments: dict[CubeCoordinate, int],
        cell: CubeCoordinate,
        variant_id: int,
    ) -> bool:
        if not domains[cell] & self.variant_bits[variant_id]:
            return False

        piece_is_already_used = any(
            self.same_piece_masks[variant_id] & self.variant_bits[assigned_variant_id]
            for assigned_variant_id in assignments.values()
        )
        if piece_is_already_used:
            return False

        domains[cell] = self.variant_bits[variant_id]
        assignments[cell] = variant_id
        if len(assignments) >= self.target_count:
            return True

        queue = [cell]

        used_piece_mask = self.same_piece_masks[variant_id]
        for other_cell in self.cells:
            if other_cell == cell or other_cell in assignments:
                continue

            before = domains[other_cell]
            domains[other_cell] &= ~used_piece_mask
            if not domains[other_cell]:
                if not self._can_still_reach_target(domains, assignments):
                    return False
                continue
            if domains[other_cell] != before:
                queue.append(other_cell)

        return self._propagate(domains, assignments, queue)

    def _can_still_reach_target(
        self,
        domains: dict[CubeCoordinate, int],
        assignments: dict[CubeCoordinate, int],
    ) -> bool:
        available_cells = sum(1 for cell in self.cells if cell in assignments or domains[cell])

        return available_cells >= self.target_count

    def _propagate(
        self,
        domains: dict[CubeCoordinate, int],
        assignments: dict[CubeCoordinate, int],
        queue: list[CubeCoordinate],
    ) -> bool:
        while queue:
            cell = queue.pop()
            if not domains[cell]:
                continue

            for direction, neighbor in self.neighbors[cell]:
                allowed_mask = 0
                for variant_id in self._iter_mask(domains[cell]):
                    allowed_mask |= self.compatible_masks_by_variant_direction[variant_id][direction]
                filtered_domain = domains[neighbor] & allowed_mask

                if not filtered_domain:
                    if neighbor in assignments:
                        return False

                    domains[neighbor] = 0
                    if not self._can_still_reach_target(domains, assignments):
                        return False
                    continue

                if filtered_domain != domains[neighbor]:
                    domains[neighbor] = filtered_domain
                    queue.append(neighbor)

        return True

    def _iter_mask(self, mask: int):
        while mask:
            bit = mask & -mask
            yield bit.bit_length() - 1
            mask ^= bit

    def _iter_direction_mask(self, mask: int):
        for direction in range(6):
            if mask & (1 << direction):
                yield direction

    def _variants_connect_by_id(self, left_variant_id: int, direction: int, right_variant_id: int) -> bool:
        left = self.variants[left_variant_id]
        right = self.variants[right_variant_id]

        return (
            edge_is_traversable(left.edges[direction])
            and left.edges[direction] == right.edges[opposite_edge(direction)]
        )
