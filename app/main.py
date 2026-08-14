from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pydantic import Field

from app.services.wfc import DEFAULT_BACKTRACK_LIMIT
from app.services.wfc import DEFAULT_RETRY_LIMIT
from app.services.wfc import generate_map


APP_DIR = Path(__file__).parent

app = FastAPI()
app.mount(
    "/assets/files",
    StaticFiles(directory=APP_DIR / "assets" / "files", check_dir=False),
    name="asset-files",
)


class GenerateMapRequest(BaseModel):
    seed: int | None = None
    retry_limit: int = Field(default=DEFAULT_RETRY_LIMIT, ge=1)
    backtrack_limit: int = Field(default=DEFAULT_BACKTRACK_LIMIT, ge=0)


class PlacementResponse(BaseModel):
    url: str
    title: str
    q: int
    r: int
    s: int
    rotation: int


class GenerateMapResponse(BaseModel):
    placements: list[PlacementResponse]
    seed: int
    radius: int
    placed_count: int


@app.get("/")
def root():
    return FileResponse(APP_DIR / "static" / "index.html")


@app.post("/maps/generate")
def generate_random_map(request: GenerateMapRequest) -> GenerateMapResponse:
    generated_map = generate_map(
        seed=request.seed,
        retry_limit=request.retry_limit,
        backtrack_limit=request.backtrack_limit,
    )

    return GenerateMapResponse(
        placements=[
            PlacementResponse(
                url=placement.url,
                title=placement.title,
                q=placement.q,
                r=placement.r,
                s=placement.s,
                rotation=placement.rotation,
            )
            for placement in generated_map.placements
        ],
        seed=generated_map.seed,
        radius=generated_map.radius,
        placed_count=generated_map.placed_count,
    )
