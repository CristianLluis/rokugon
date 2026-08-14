import unittest

from fastapi.testclient import TestClient

from app.main import app


class MapsApiTestCase(unittest.TestCase):
    def test_root_returns_pixi_page(self):
        client = TestClient(app)

        response = client.get("/")

        self.assertEqual(200, response.status_code)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("pixi.js", response.text)
        self.assertIn("Generate", response.text)

    def test_generate_map_returns_flat_top_cube_placements(self):
        client = TestClient(app)

        response = client.post(
            "/maps/generate",
            json={
                "seed": 123,
                "retry_limit": 1,
                "backtrack_limit": 200,
            },
        )

        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertEqual(123, data["seed"])
        self.assertEqual(data["placed_count"], len(data["placements"]))
        self.assertGreater(data["placed_count"], 0)

        for placement in data["placements"]:
            self.assertEqual(0, placement["q"] + placement["r"] + placement["s"])
            self.assertLessEqual(max(abs(placement["q"]), abs(placement["r"]), abs(placement["s"])), data["radius"])
            self.assertTrue(placement["url"].startswith("/assets/files/"))
            self.assertTrue(placement["url"].endswith(".png"))
            self.assertEqual(placement["url"].rsplit("/", 1)[-1], placement["title"])
            self.assertGreaterEqual(placement["rotation"], 0)
            self.assertLessEqual(placement["rotation"], 5)
