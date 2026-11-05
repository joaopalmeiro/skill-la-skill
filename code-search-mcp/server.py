from functools import cache
from pathlib import Path

import numpy as np
import numpy.typing as npt
from mcp.server import MCPServer
from rgapi import fd
from sentence_transformers import SentenceTransformer

ROOT = Path("/Users/joao.palmeiro/Documents/GitHub")
REPOS = ["python-playground"]
INDEX_PATH = Path(__file__).parent / "index.npz"

SKIP_DIRS = [".git", ".venv"]

model = SentenceTransformer(
    "google/embeddinggemma-2",
    revision="914f7f89142e33e77833254d9c9b90c3cef7303b",
    config_kwargs={"vision_config": None, "audio_config": None},
    processor_kwargs={"model_max_length": 8192},
)

mcp = MCPServer("code-search")


@cache
def load_index() -> tuple[list[str], npt.NDArray[np.float32]]:
    if INDEX_PATH.exists():
        data = np.load(INDEX_PATH)
        return data["paths"].tolist(), data["embeddings"]

    # `hidden=True` walks dot-folders too, so only the ones in `SKIP_DIRS` are skipped (with their subtrees).
    files: list[Path] = fd(root=[ROOT / repo for repo in REPOS], ext="py", hidden=True, skip_dir=SKIP_DIRS)

    documents = [f"title: {file.relative_to(ROOT)} | text: {file.read_text()}" for file in files]
    embeddings = model.encode(documents, batch_size=4, show_progress_bar=True)
    paths = [str(file) for file in files]

    np.savez(INDEX_PATH, paths=np.array(paths), embeddings=embeddings)

    return paths, embeddings


@mcp.tool()
def search_code(query: str, top_k: int = 5) -> str:
    """Semantic search over the Python files of selected local repos. Returns the most relevant file paths."""
    paths, embeddings = load_index()
    query_embedding = model.encode(query, prompt_name="CodeRetrieval", show_progress_bar=False)

    scores = model.similarity(query_embedding, embeddings)[0]
    top = scores.topk(top_k)

    return "\n".join(
        f"{score:.3f} {paths[i]}" for score, i in zip(top.values.tolist(), top.indices.tolist(), strict=True)
    )


if __name__ == "__main__":
    load_index()
