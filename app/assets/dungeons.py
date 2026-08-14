from app.models.tiles import Edge


DUNGEON_TERRAIN = [
    {
        "front": {
            "image": "dungeons_01_033.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 2,
        },
        "back": {
            "image": "dungeons_01_034.png",
            "edges": (
                Edge.CAVE,
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
            "image": "dungeons_02_035.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "dungeons_02_036.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "dungeons_03_037.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.CAVE,
            ),
            "weight": 3,
        },
        "back": {
            "image": "dungeons_03_038.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "dungeons_04_039.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 6,
        },
        "back": {
            "image": "dungeons_04_040.png",
            "edges": (
                Edge.CAVE,
                Edge.CAVE,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "dungeons_05_041.png",
            "edges": (
                Edge.DUNGEON,
                Edge.CAVE,
                Edge.CAVE,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 3,
        },
        "back": {
            "image": "dungeons_05_042.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "dungeons_06_043.png",
            "edges": (
                Edge.CAVE,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.CAVE,
                Edge.DUNGEON,
                Edge.WALL,
            ),
            "weight": 3,
        },
        "back": {
            "image": "dungeons_06_044.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.CAVE,
                Edge.WALL,
                Edge.DUNGEON,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "dungeons_07_045.png",
            "edges": (
                Edge.DUNGEON,
                Edge.CAVE,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 3,
        },
        "back": {
            "image": "dungeons_07_046.png",
            "edges": (
                Edge.DUNGEON,
                Edge.CAVE,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "dungeons_08_047.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 2,
        },
        "back": {
            "image": "dungeons_08_048.png",
            "edges": (
                Edge.DUNGEON,
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
            "image": "dungeons_09_049.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 2,
        },
        "back": {
            "image": "dungeons_09_050.png",
            "edges": (
                Edge.DUNGEON,
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
            "image": "dungeons_10_051.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 2,
        },
        "back": {
            "image": "dungeons_10_052.png",
            "edges": (
                Edge.DUNGEON,
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
            "image": "dungeons_11_053.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "dungeons_11_054.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "dungeons_12_055.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "dungeons_12_056.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "dungeons_13_057.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "dungeons_13_058.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "dungeons_14_059.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "dungeons_14_060.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "dungeons_15_061.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
            ),
            "weight": 6,
        },
        "back": {
            "image": "dungeons_15_062.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.DUNGEON,
                Edge.WALL,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "dungeons_16_063.png",
            "edges": (
                Edge.DUNGEON,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "dungeons_16_064.png",
            "edges": (
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.DUNGEON,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "dungeons_17_065.png",
            "edges": (
                Edge.DUNGEON,
                Edge.DUNGEON,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 6,
        },
        "back": {
            "image": "dungeons_17_065.png",
            "edges": (
                Edge.DUNGEON,
                Edge.DUNGEON,
                Edge.DUNGEON,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 6,
        },
    },
]
