# code-search-mcp

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

## Usage

### Kiro

```bash
code ~/.kiro/settings/mcp.json
```

```json
{
  "mcpServers": {
    "code-search": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/joao.palmeiro/Documents/GitHub/skill-la-skill/code-search-mcp",
        "mcp",
        "run",
        "server.py"
      ],
      "disabled": false,
      "autoApprove": ["search_code"]
    }
  }
}
```

## Development

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (if necessary):

```bash
curl -LsSf https://astral.sh/uv/0.11.6/install.sh | sh
```

```bash
uv python install
```

```bash
uv audit --verbose
```

```bash
uv run mcp dev server.py
```

```bash
uv run mypy
```

```bash
uv run ruff format
```

```bash
uv run ruff check --fix
```
