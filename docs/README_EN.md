<p align="center">
  <b>OpenNews MCP Server</b><br>
  Crypto News Aggregation · AI Ratings · Trading Signals · Real-time Feeds
</p>

<p align="center">
  <a href="../README.md">中文</a> | <a href="./README_JA.md">日本語</a> | <a href="./README_KO.md">한국어</a>
</p>

---

## Quick Install

> **Trial period**: A free public API Key is provided — copy and use, no sign-up required.

### Claude Code

```bash
claude mcp add opennews \
  -e OPENNEWS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c \
  -- uv --directory /path/to/opennews-mcp run opennews-mcp
```

> Replace `/path/to/opennews-mcp` with your local project path.

### OpenClaw

```bash
export OPENNEWS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
cp -r openclaw-skill/opennews ~/.openclaw/skills/
```

> The above uses a free trial Token. After the trial period, replace it with your own Key. See [Configuration](#configuration).

---

## Let AI Review & Install For You

Not sure if this MCP is safe? Paste the prompt below to your AI assistant — it will review the source code first, then install if safe:

> **Copy this prompt and send it to your AI assistant (replace `<project-path>` with the actual path):**

```text
Please review and install the opennews-mcp MCP server for me. The project is at <project-path>.

Steps:
1. Review these files for security:
   - src/opennews_mcp/api_client.py — Confirm it only connects to ai.6551.io, no data sent elsewhere
   - src/opennews_mcp/config.py — Confirm token is only read from local config.json or env vars, no hardcoded secrets or leaks
   - src/opennews_mcp/tools/*.py — Confirm all tools only perform API queries, no file writes, command execution, or dangerous operations
   - pyproject.toml — Confirm dependencies are only mcp, httpx, websockets, no suspicious packages
2. Tell me your conclusion: safe / risky / problematic, with specific reasons
3. If safe, run the install (using the free trial Token):
   claude mcp add opennews -e OPENNEWS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c -- uv --directory <project-path> run opennews-mcp
```

---

## What Can It Do?

Once connected, just ask your AI assistant:

| You say | It does |
|---------|---------|
| "Latest crypto news" | Fetches newest articles |
| "Search for SEC regulation news" | Full-text keyword search |
| "BTC related news" | Filter by coin |
| "Bloomberg articles" | Filter by source |
| "On-chain events" | Filter by engine type (onchain) |
| "High-impact news, AI score above 80" | High-score filtering |
| "Bullish signals" | Filter by trading signal (long) |
| "Subscribe to live news" | WebSocket real-time feed |

---

## Available Tools

| Category | Tool | Description |
|----------|------|-------------|
| Discovery | `get_news_sources` | All news source categories as a tree |
| | `list_news_types` | All available source codes |
| Search | `get_latest_news` | Latest articles |
| | `search_news` | Keyword search |
| | `search_news_by_coin` | By coin (BTC, ETH, SOL...) |
| | `get_news_by_source` | By source (Bloomberg, Reuters...) |
| | `get_news_by_engine` | By type (news, listing, onchain, meme, market) |
| | `search_news_by_date` | Date range + coin/keyword |
| AI | `get_high_score_news` | Articles with score >= threshold |
| | `get_news_by_signal` | By signal: long / short / neutral |
| Real-time | `subscribe_latest_news` | WebSocket live collection |

---

## Configuration

### Free Trial Token

Currently in trial period. You can use this public Token directly:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c
```

Set the environment variable:

```bash
# macOS / Linux
export OPENNEWS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"

# Windows PowerShell
$env:OPENNEWS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
```

> Replace with your own Token after the trial period ends.

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENNEWS_TOKEN` | **Yes** | 6551 API Bearer Token (free trial Key available above) |
| `OPENNEWS_API_BASE` | No | Override REST API URL |
| `OPENNEWS_WSS_URL` | No | Override WebSocket URL |
| `OPENNEWS_MAX_ROWS` | No | Max results per query (default: 100) |

Also supports `config.json` in the project root (env vars take precedence):

```json
{
  "api_base_url": "https://ai.6551.io/news-platform",
  "wss_url": "wss://ai.6551.io/news-platform/rpc",
  "api_token": "your-api-token-here",
  "max_rows": 100
}
```

---

## Data Structure

Each article:

```json
{
  "id": "unique-article-id",
  "text": "Headline / content",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [{ "symbol": "BTC", "market_type": "spot", "match": "title" }],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long",
    "status": "done",
    "summary": "Chinese summary",
    "enSummary": "English summary"
  },
  "ts": 1708473600000
}
```

| AI Field | Description |
|----------|-------------|
| `score` | 0-100 impact rating |
| `signal` | `long` (bullish) / `short` (bearish) / `neutral` |
| `status` | `done` = AI analysis complete |

---

<details>
<summary><b>Other Clients — Manual Install</b> (click to expand)</summary>

> In all configs below, replace `/path/to/opennews-mcp` with your actual local project path. The `OPENNEWS_TOKEN` value can use the free trial Token above.

### Claude Desktop

Edit config (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`, Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
      }
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json` or Settings > MCP Servers:

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
      }
    }
  }
}
```

### Windsurf

`~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
      }
    }
  }
}
```

### Cline

VS Code sidebar > Cline > MCP Servers > Configure, edit `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Continue.dev

`~/.continue/config.yaml`:

```yaml
mcpServers:
  - name: opennews
    command: uv
    args:
      - --directory
      - /path/to/opennews-mcp
      - run
      - opennews-mcp
    env:
      OPENNEWS_TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c
```

### Cherry Studio

Settings > MCP Servers > Add > Type stdio: Command `uv`, Args `--directory /path/to/opennews-mcp run opennews-mcp`, Env `OPENNEWS_TOKEN`.

### Zed Editor

`~/.config/zed/settings.json`:

```json
{
  "context_servers": {
    "opennews": {
      "command": {
        "path": "uv",
        "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
        "env": {
          "OPENNEWS_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
        }
      }
    }
  }
}
```

### Any stdio MCP client

```bash
OPENNEWS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c \
  uv --directory /path/to/opennews-mcp run opennews-mcp
```

</details>

---

## Compatibility

| Client | Install Method | Status |
|--------|---------------|--------|
| **Claude Code** | `claude mcp add` | One-liner |
| **OpenClaw** | Copy skill directory | One-liner |
| Claude Desktop | JSON config | Supported |
| Cursor | JSON config | Supported |
| Windsurf | JSON config | Supported |
| Cline | JSON config | Supported |
| Continue.dev | YAML / JSON | Supported |
| Cherry Studio | GUI | Supported |
| Zed | JSON config | Supported |

---

## Development

```bash
cd /path/to/opennews-mcp
uv sync
uv run opennews-mcp
```

```bash
# MCP Inspector
npx @modelcontextprotocol/inspector uv --directory /path/to/opennews-mcp run opennews-mcp
```

### Project Structure

```
├── README.md                  # 中文 (default)
├── docs/
│   ├── README_EN.md           # English
│   ├── README_JA.md           # 日本語
│   └── README_KO.md           # 한국어
├── openclaw-skill/opennews/   # OpenClaw Skill
├── knowledge/guide.md         # Embedded knowledge
├── pyproject.toml
├── config.json
└── src/opennews_mcp/
    ├── server.py              # Entry point
    ├── app.py                 # FastMCP instance
    ├── config.py              # Config loader
    ├── api_client.py          # HTTP + WebSocket
    └── tools/                 # 11 tools
```

## License

MIT
