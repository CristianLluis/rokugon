from app.models.tiles import Edge


CAVERN_TERRAIN = [
    {
        "front": {
            "image": "caverns_01_001.png",
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
            "image": "caverns_01_002.png",
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
            "image": "caverns_02_003.png",
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
            "image": "caverns_02_004.png",
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
            "image": "caverns_03_005.png",
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
            "image": "caverns_03_006.png",
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
            "image": "caverns_04_007.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 8,
        },
        "back": {
            "image": "caverns_04_008.png",
            "edges": (
                Edge.CAVE,
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
            "image": "caverns_05_009.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 8,
        },
        "back": {
            "image": "caverns_05_010.png",
            "edges": (
                Edge.CAVE,
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
            "image": "caverns_06_011.png",
            "edges": (
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 6,
        },
        "back": {
            "image": "caverns_06_012.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "caverns_07_013.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "caverns_07_014.png",
            "edges": (
                Edge.CAVE,
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
            "image": "caverns_08_015.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
            ),
            "weight": 8,
        },
        "back": {
            "image": "caverns_08_016.png",
            "edges": (
                Edge.CAVE,
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
            "image": "caverns_09_017.png",
            "edges": (
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 3,
        },
        "back": {
            "image": "caverns_09_018.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.WALL,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "caverns_10_019.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 8,
        },
        "back": {
            "image": "caverns_10_020.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "caverns_11_021.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 8,
        },
        "back": {
            "image": "caverns_11_022.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 8,
        },
    },
    {
        "front": {
            "image": "caverns_12_023.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 6,
        },
        "back": {
            "image": "caverns_12_024.png",
            "edges": (
                Edge.CAVE,
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.WALL,
            ),
            "weight": 3,
        },
    },
    {
        "front": {
            "image": "caverns_13_025.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 6,
        },
        "back": {
            "image": "caverns_13_026.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "caverns_14_027.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
            ),
            "weight": 6,
        },
        "back": {
            "image": "caverns_14_028.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.WALL,
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 6,
        },
    },
    {
        "front": {
            "image": "caverns_15_029.png",
            "edges": (
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 1,
        },
        "back": {
            "image": "caverns_15_030.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 1,
        },
    },
    {
        "front": {
            "image": "caverns_16_031.png",
            "edges": (
                Edge.WALL,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 1,
        },
        "back": {
            "image": "caverns_16_032.png",
            "edges": (
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
                Edge.CAVE,
            ),
            "weight": 1,
        },
    },
]
