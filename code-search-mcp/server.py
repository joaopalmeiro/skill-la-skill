from pathlib import Path

from lancedb import LanceDBConnection
from lancedb.table import LanceTable
from mcp.server import MCPServer
from rgapi import fd
from sentence_transformers import SentenceTransformer

ROOT = Path("/Users/joao.palmeiro/Documents/GitHub")
REPOS = ["python-playground"]
DB_PATH = Path(__file__).parent / "index.lancedb"
TABLE_NAME = "files"

SKIP_DIRS = [".git", ".venv"]

model = SentenceTransformer(
    "google/embeddinggemma-2",
    revision="914f7f89142e33e77833254d9c9b90c3cef7303b",
    config_kwargs={"vision_config": None, "audio_config": None},
    processor_kwargs={"model_max_length": 8192},
)

mcp = MCPServer("code-search")


def load_index() -> LanceTable:
    # `lancedb.connect` returns the generic `DBConnection`, whose tables don't type vector queries.
    db = LanceDBConnection(DB_PATH)
    if TABLE_NAME in db.list_tables().tables:
        return db.open_table(TABLE_NAME)

    # `hidden=True` walks dot-folders too, so only the ones in `SKIP_DIRS` are skipped (with their subtrees).
    files: list[Path] = fd(root=[ROOT / repo for repo in REPOS], ext="py", hidden=True, skip_dir=SKIP_DIRS)

    documents = [f"title: {file.relative_to(ROOT)} | text: {file.read_text()}" for file in files]
    embeddings = model.encode(documents, batch_size=4, show_progress_bar=True)

    # Each row keeps the file path next to its vector, so no separate metadata file is needed.
    rows = [{"path": str(file), "vector": embedding} for file, embedding in zip(files, embeddings, strict=True)]
    return db.create_table(TABLE_NAME, data=rows)


@mcp.tool()
def search_code(query: str, top_k: int = 5) -> str:
    """Semantic search over the Python files of selected local repos. Returns the most relevant file paths."""
    table = load_index()
    query_embedding = model.encode(query, prompt_name="CodeRetrieval", show_progress_bar=False)

    # Without a vector index, LanceDB compares the query against every row (exact search).
    results = table.search(query_embedding).distance_type("cosine").select(["path", "_distance"]).limit(top_k).to_list()

    # Cosine distance is `1 - cosine similarity`, so convert it back to a similarity score.
    return "\n".join(f"{1 - row['_distance']:.3f} {row['path']}" for row in results)


if __name__ == "__main__":
    load_index()
