from app.models.tiles import Edge


RIVERS_TERRAIN = [
    {
        "front": {
            "image": "rivers_01_067.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 2,
        },
        "back": {
            "image": "rivers_01_068.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 2,
        },
    },
    {
        "front": {
            "image": "rivers_02_069.png",
            "edges": (
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 8,
        },
        "back": {
            "image": "rivers_02_070.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WATER,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "rivers_03_071.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "rivers_03_072.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "rivers_04_073.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "rivers_04_074.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "rivers_05_075.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
            ),
            "weight": 3,
        },
        "back": {
            "image": "rivers_05_076.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "rivers_06_077.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.CAVE,
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
            ),
            "weight": 3,
        },
        "back": {
            "image": "rivers_06_078.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "rivers_07_079.png",
            "edges": (
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "rivers_07_080.png",
            "edges": (
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
                Edge.WATER,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "rivers_08_081.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
            ),
            "weight": 3,
        },
        "back": {
            "image": "rivers_08_082.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.CAVE,
                Edge.WATER,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "rivers_09_083.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 8,
        },
        "back": {
            "image": "rivers_09_084.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "rivers_10_085.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 6,
        },
        "back": {
            "image": "rivers_10_086.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WATER,
                Edge.WALL,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "rivers_11_087.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 3,
        },
        "back": {
            "image": "rivers_11_088.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
                Edge.WATER,
                Edge.WALL,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "rivers_12_089.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 6,
        },
        "back": {
            "image": "rivers_12_090.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WATER,
                Edge.WATER,
                Edge.WALL,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "rivers_13_091.png",
            "edges": (
                Edge.WATER,
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
            ),
            "weight": 6,
        },
        "back": {
            "image": "rivers_13_092.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WATER,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "rivers_14_093.png",
            "edges": (
                Edge.WATER,
                Edge.WATER,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 3,
        },
        "back": {
            "image": "rivers_14_094.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WATER,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "rivers_15_095.png",
            "edges": (
                Edge.WATER,
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 6,
        },
        "back": {
            "image": "rivers_15_096.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WATER,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "rivers_16_097.png",
            "edges": (
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 6,
        },
        "back": {
            "image": "rivers_16_098.png",
            "edges": (
                Edge.WATER,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WATER,
                Edge.WATER,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "rivers_17_099.png",
            "edges": (
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 1,
        },
        "back": {
            "image": "rivers_17_100.png",
            "edges": (
                Edge.WATER,
                Edge.CAVE,
                Edge.WALL,
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
            ),
            "weight": 1,
        },
    },
    {
        "front": {
            "image": "rivers_18_101.png",
            "edges": (
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 1,
        },
        "back": {
            "image": "rivers_18_102.png",
            "edges": (
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
                Edge.WATER,
            ),
            "weight": 1,
        },
    },
]
