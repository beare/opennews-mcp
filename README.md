<p align="center">
  <b>OpenNews MCP Server</b><br>
  加密货币新闻聚合 · AI 评分 · 交易信号 · 实时推送
</p>

<p align="center">
  <a href="./docs/README_EN.md">English</a> | <a href="./docs/README_JA.md">日本語</a> | <a href="./docs/README_KO.md">한국어</a>
</p>

---

## 快速安装

> **首先前往 [https://6551.io/mcp](https://6551.io/mcp) 申请你的 API Token。**

### Claude Code

```bash
claude mcp add opennews \
  -e OPENNEWS_TOKEN=<your-token> \
  -- uv --directory /path/to/opennews-mcp run opennews-mcp
```

> `/path/to/opennews-mcp` 替换为你本地的项目路径，`<your-token>` 替换为你申请的 Token。

### OpenClaw

```bash
export OPENNEWS_TOKEN="<your-token>"
cp -r openclaw-skill/opennews ~/.openclaw/skills/
```

---

## 让 AI 帮你审查并安装

不确定这个 MCP 是否安全？把下面这段 prompt 发给你的 AI 助手，让它先审查源码再决定是否安装：

> **复制下方 prompt，粘贴给你的 AI 助手（将 `<项目路径>` 和 `<your-token>` 替换为实际值）：**

```text
请帮我审查并安装 opennews-mcp 这个 MCP server。项目在本地 <项目路径> 目录。

步骤：
1. 审查项目内包括但不限于以下文件的安全性：
   - src/opennews_mcp/api_client.py — 确认只连接了 ai.6551.io，没有向其他地址发送数据
   - src/opennews_mcp/config.py — 确认 token 只从本地 config.json 或环境变量读取，没有硬编码或外泄
   - src/opennews_mcp/tools/*.py — 确认所有工具只做 API 查询，没有文件写入、命令执行或其他危险操作
   - pyproject.toml — 确认依赖项只有 mcp、httpx、websockets，没有可疑包
2. 告诉我审查结论：安全/有风险/有问题，以及具体理由
3. 如果安全，帮我执行安装（Token 从 https://6551.io/mcp 申请）：
   claude mcp add opennews -e OPENNEWS_TOKEN=<your-token> -- uv --directory <项目路径> run opennews-mcp
```

---

## 它能做什么？

连接后，直接对你的 AI 助手说：

| 你说 | 它做 |
|------|------|
| "最新的加密货币新闻" | 获取最新文章 |
| "搜索 SEC 监管相关新闻" | 全文关键词搜索 |
| "BTC 相关新闻" | 按币种过滤 |
| "Bloomberg 的文章" | 按来源过滤 |
| "链上事件" | 按引擎类型过滤（onchain） |
| "AI 评分 80 以上的重要新闻" | 高分筛选 |
| "看多信号" | 按交易信号过滤（long） |
| "订阅实时新闻" | WebSocket 实时推送 |
| "查看 elonmusk 的 Twitter 资料" | 获取 Twitter 用户信息 |
| "elonmusk 最近发了什么推文" | 获取用户推文 |
| "搜索 Bitcoin 相关推文" | Twitter 关键词搜索 |

---

## 可用工具一览

| 类别 | 工具 | 说明 |
|------|------|------|
| 发现 | `get_news_sources` | 获取所有新闻源分类树 |
| | `list_news_types` | 所有可用的新闻源代码 |
| 搜索 | `get_latest_news` | 最新文章 |
| | `search_news` | 关键词搜索 |
| | `search_news_by_coin` | 按币种（BTC, ETH, SOL...） |
| | `get_news_by_source` | 按引擎类型和来源（需指定 engine_type 和 news_type） |
| | `get_news_by_engine` | 按类型（news, listing, onchain, meme, market） |
| | `search_news_advanced` | 高级搜索（多过滤器组合） |
| AI | `get_high_score_news` | 评分 >= 阈值的文章 |
| | `get_news_by_signal` | 按信号：long / short / neutral |
| 实时 | `subscribe_latest_news` | WebSocket 实时收集 |
| Twitter | `get_twitter_user` | 获取 Twitter 用户资料 |
| | `get_twitter_user_by_id` | 通过 ID 获取用户资料 |
| | `get_twitter_user_tweets` | 获取用户推文 |
| | `search_twitter` | Twitter 搜索 |
| | `search_twitter_advanced` | Twitter 高级搜索（多过滤器） |

---

## 配置

### 获取 API Token

前往 [https://6551.io/mcp](https://6551.io/mcp) 申请你的 API Token。

设置环境变量：

```bash
# macOS / Linux
export OPENNEWS_TOKEN="<your-token>"

# Windows PowerShell
$env:OPENNEWS_TOKEN = "<your-token>"
```

| 变量 | 必填 | 说明 |
|------|------|------|
| `OPENNEWS_TOKEN` | **是** | 6551 API Bearer Token（从 https://6551.io/mcp 申请） |
| `OPENNEWS_API_BASE` | 否 | 覆盖 REST API 地址 |
| `OPENNEWS_WSS_URL` | 否 | 覆盖 WebSocket 地址 |
| `OPENNEWS_MAX_ROWS` | 否 | 单次最大结果数（默认 100） |

也支持项目根目录 `config.json`（环境变量优先级更高）：

```json
{
  "api_base_url": "https://ai.6551.io",
  "wss_url": "wss://ai.6551.io/open/news_wss",
  "api_token": "<your-token>",
  "max_rows": 100
}
```

---

## 数据结构

每篇文章返回格式：

```json
{
  "id": "unique-article-id",
  "text": "标题 / 内容",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [{ "symbol": "BTC", "market_type": "spot", "match": "title" }],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long",
    "status": "done",
    "summary": "中文摘要",
    "enSummary": "English summary"
  },
  "ts": 1708473600000
}
```

| AI 字段 | 说明 |
|---------|------|
| `score` | 0-100 影响力评分 |
| `signal` | `long`（看多）/ `short`（看空）/ `neutral` |
| `status` | `done` = AI 分析已完成 |

---

<details>
<summary><b>其他客户端手动安装</b>（点击展开）</summary>

> 以下所有配置中 `/path/to/opennews-mcp` 需替换为你本地的实际项目路径，`<your-token>` 替换为你从 [https://6551.io/mcp](https://6551.io/mcp) 申请的 Token。

### Claude Desktop

编辑配置文件（macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`，Windows: `%APPDATA%\Claude\claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Cursor

`~/.cursor/mcp.json` 或 Settings > MCP Servers：

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Windsurf

`~/.codeium/windsurf/mcp_config.json`：

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      }
    }
  }
}
```

### Cline

VS Code 侧栏 > Cline > MCP Servers > Configure，编辑 `cline_mcp_settings.json`：

```json
{
  "mcpServers": {
    "opennews": {
      "command": "uv",
      "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
      "env": {
        "OPENNEWS_TOKEN": "<your-token>"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Continue.dev

`~/.continue/config.yaml`：

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
      OPENNEWS_TOKEN: <your-token>
```

### Cherry Studio

设置 > MCP 服务器 > 添加 > 类型 stdio：Command `uv`，Args `--directory /path/to/opennews-mcp run opennews-mcp`，Env `OPENNEWS_TOKEN`。

### Zed Editor

`~/.config/zed/settings.json`：

```json
{
  "context_servers": {
    "opennews": {
      "command": {
        "path": "uv",
        "args": ["--directory", "/path/to/opennews-mcp", "run", "opennews-mcp"],
        "env": {
          "OPENNEWS_TOKEN": "<your-token>"
        }
      }
    }
  }
}
```

### 任意 stdio MCP 客户端

```bash
OPENNEWS_TOKEN=<your-token> \
  uv --directory /path/to/opennews-mcp run opennews-mcp
```

</details>

---

## 兼容性

| 客户端 | 安装方式 | 状态 |
|--------|----------|------|
| **Claude Code** | `claude mcp add` | 一键安装 |
| **OpenClaw** | 复制 Skill 目录 | 一键安装 |
| Claude Desktop | JSON 配置 | 支持 |
| Cursor | JSON 配置 | 支持 |
| Windsurf | JSON 配置 | 支持 |
| Cline | JSON 配置 | 支持 |
| Continue.dev | YAML / JSON | 支持 |
| Cherry Studio | GUI | 支持 |
| Zed | JSON 配置 | 支持 |

---

## 开发

```bash
cd /path/to/opennews-mcp
uv sync
uv run opennews-mcp
```

```bash
# MCP Inspector 测试
npx @modelcontextprotocol/inspector uv --directory /path/to/opennews-mcp run opennews-mcp
```

### 项目结构

```
├── README.md                  # 中文（默认）
├── docs/
│   ├── README_EN.md           # English
│   ├── README_JA.md           # 日本語
│   └── README_KO.md           # 한국어
├── openclaw-skill/opennews/   # OpenClaw Skill
├── knowledge/guide.md         # 嵌入式知识
├── pyproject.toml
├── config.json
└── src/opennews_mcp/
    ├── server.py              # 入口
    ├── app.py                 # FastMCP 实例
    ├── config.py              # 配置加载
    ├── api_client.py          # HTTP + WebSocket
    └── tools/                 # 11 个工具
```

## 许可证

MIT
