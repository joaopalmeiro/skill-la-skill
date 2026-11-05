from pathlib import Path
from typing import TypedDict

from lancedb import LanceDBConnection
from lancedb.table import LanceTable
from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from rgapi import fd
from sentence_transformers import SentenceTransformer

ROOT = Path("/Users/joao.palmeiro/Documents/GitHub")
REPOS = ["ai-playground", "python-playground"]

DB_PATH = Path(__file__).parent / "index"
TABLE_NAME = "files"

SKIP_DIRS = [".git", ".venv"]

model = SentenceTransformer(
    "google/embeddinggemma-2",
    revision="914f7f89142e33e77833254d9c9b90c3cef7303b",
    config_kwargs={"vision_config": None, "audio_config": None},
    processor_kwargs={"model_max_length": 8192, "truncation_side": "right"},
)

mcp = MCPServer("Code Search")


class Hit(TypedDict):
    path: str
    score: float


def build_index(db: LanceDBConnection) -> LanceTable:
    files: list[Path] = fd(root=[ROOT / repo for repo in REPOS], ext=["py"], hidden=True, skip_dir=SKIP_DIRS)

    documents = [f"title: {file.relative_to(ROOT)} | text: {file.read_text()}" for file in files]
    embeddings = model.encode(documents, batch_size=1, show_progress_bar=True)

    rows = [{"path": str(file), "vector": embedding} for file, embedding in zip(files, embeddings, strict=True)]
    return db.create_table(TABLE_NAME, data=rows, mode="overwrite")


def load_index() -> LanceTable:
    db = LanceDBConnection(DB_PATH)
    try:
        return db.open_table(TABLE_NAME)
    except ValueError:
        return build_index(db)


@mcp.tool(
    description="Search the user's personal projects for existing code to use as reference.",
    annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
)
def search_code(query: str, top_k: int = 5) -> list[Hit]:
    table = load_index()
    query_embedding = model.encode(query, prompt_name="CodeRetrieval", show_progress_bar=False)

    results = table.search(query_embedding).distance_type("cosine").select(["path", "_distance"]).limit(top_k).to_list()

    return [{"path": row["path"], "score": 1 - row["_distance"]} for row in results]


if __name__ == "__main__":
    build_index(LanceDBConnection(DB_PATH))
