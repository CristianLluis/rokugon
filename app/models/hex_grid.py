from dataclasses import dataclass


@dataclass(frozen=True, order=True, slots=True)
class CubeCoordinate:
    q: int
    r: int
    s: int

    def __post_init__(self):
        if self.q + self.r + self.s != 0:
            raise ValueError("cube coordinates must satisfy q + r + s == 0")

    def neighbor(self, direction: int) -> CubeCoordinate:
        dq, dr, ds = CUBE_DIRECTIONS[direction]
        return CubeCoordinate(self.q + dq, self.r + dr, self.s + ds)


CUBE_DIRECTIONS = (
    (0, -1, 1),  # top
    (1, -1, 0),  # upper-right
    (1, 0, -1),  # lower-right
    (0, 1, -1),  # bottom
    (-1, 1, 0),  # lower-left
    (-1, 0, 1),  # upper-left
)


def opposite_edge(direction: int) -> int:
    return (direction + 3) % 6


def cube_radius(radius: int) -> tuple[CubeCoordinate, ...]:
    if radius < 0:
        raise ValueError("radius must be greater than or equal to 0")

    coordinates = []
    for q in range(-radius, radius + 1):
        r_min = max(-radius, -q - radius)
        r_max = min(radius, -q + radius)
        for r in range(r_min, r_max + 1):
            coordinates.append(CubeCoordinate(q=q, r=r, s=-q - r))

    return tuple(sorted(coordinates))
