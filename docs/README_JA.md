<p align="center">
  <b>OpenNews MCP Server</b><br>
  暗号通貨ニュース集約 · AI 評価 · トレーディングシグナル · リアルタイムフィード
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="./README_KO.md">한국어</a>
</p>

---

## クイックインストール

> **トライアル期間**：無料の公開 API Key を提供しています。コピーしてすぐに使えます。登録不要。

### Claude Code

```bash
claude mcp add opennews \
  -e OPENNEWS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c \
  -- uv --directory /path/to/opennews-mcp run opennews-mcp
```

> `/path/to/opennews-mcp` をローカルのプロジェクトパスに置き換えてください。

### OpenClaw

```bash
export OPENNEWS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
cp -r openclaw-skill/opennews ~/.openclaw/skills/
```

> 上記は無料トライアル Token です。トライアル期間終了後はご自身の Key に置き換えてください。[設定](#設定)を参照。

---

## AI にレビュー＆インストールしてもらう

この MCP が安全かどうか不安ですか？以下のプロンプトを AI アシスタントに送信すれば、ソースコードをレビューしてからインストールしてくれます：

> **以下のプロンプトをコピーして AI アシスタントに送信してください（`<プロジェクトパス>` を実際のパスに置き換え）：**

```text
opennews-mcp という MCP サーバーをレビューしてインストールしてください。プロジェクトはローカルの <プロジェクトパス> にあります。

手順：
1. 以下のファイルのセキュリティを確認：
   - src/opennews_mcp/api_client.py — ai.6551.io のみに接続し、他のアドレスにデータを送信していないことを確認
   - src/opennews_mcp/config.py — トークンがローカルの config.json または環境変数からのみ読み取られ、ハードコードや漏洩がないことを確認
   - src/opennews_mcp/tools/*.py — すべてのツールが API クエリのみを実行し、ファイル書き込み、コマンド実行、その他の危険な操作がないことを確認
   - pyproject.toml — 依存関係が mcp、httpx、websockets のみで、不審なパッケージがないことを確認
2. レビュー結論を教えてください：安全 / リスクあり / 問題あり、具体的な理由とともに
3. 安全であれば、インストールを実行（無料トライアル Token を使用）：
   claude mcp add opennews -e OPENNEWS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c -- uv --directory <プロジェクトパス> run opennews-mcp
```

---

## 何ができる？

接続後、AI アシスタントに話しかけるだけ：

| あなたが言う | 実行される操作 |
|-------------|---------------|
| 「最新の暗号通貨ニュース」 | 最新記事を取得 |
| 「SEC 規制のニュースを検索」 | 全文キーワード検索 |
| 「BTC 関連ニュース」 | 通貨でフィルタ |
| 「Bloomberg の記事」 | ソースでフィルタ |
| 「オンチェーンイベント」 | エンジンタイプでフィルタ（onchain） |
| 「AI スコア 80 以上の重要ニュース」 | 高スコアフィルタ |
| 「強気シグナル」 | トレーディングシグナルでフィルタ（long） |
| 「リアルタイムニュースを購読」 | WebSocket リアルタイムフィード |

---

## 利用可能なツール

| カテゴリ | ツール | 説明 |
|---------|--------|------|
| ディスカバリー | `get_news_sources` | 全ニュースソースカテゴリツリー |
| | `list_news_types` | 利用可能なソースコード一覧 |
| 検索 | `get_latest_news` | 最新記事 |
| | `search_news` | キーワード検索 |
| | `search_news_by_coin` | 通貨別（BTC, ETH, SOL...） |
| | `get_news_by_source` | ソース別（Bloomberg, Reuters...） |
| | `get_news_by_engine` | タイプ別（news, listing, onchain, meme, market） |
| | `search_news_by_date` | 日付範囲 + 通貨/キーワード |
| AI | `get_high_score_news` | スコア >= 閾値の記事 |
| | `get_news_by_signal` | シグナル別：long / short / neutral |
| リアルタイム | `subscribe_latest_news` | WebSocket ライブ収集 |

---

## 設定

### 無料トライアル Token

現在トライアル期間中です。以下の公開 Token をそのまま使えます：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c
```

環境変数を設定：

```bash
# macOS / Linux
export OPENNEWS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"

# Windows PowerShell
$env:OPENNEWS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
```

> トライアル期間終了後はご自身の Token に置き換えてください。

| 変数 | 必須 | 説明 |
|------|------|------|
| `OPENNEWS_TOKEN` | **はい** | 6551 API Bearer トークン（上記の無料 Key が利用可能） |
| `OPENNEWS_API_BASE` | いいえ | REST API URL のオーバーライド |
| `OPENNEWS_WSS_URL` | いいえ | WebSocket URL のオーバーライド |
| `OPENNEWS_MAX_ROWS` | いいえ | クエリあたりの最大結果数（デフォルト: 100） |

プロジェクトルートの `config.json` もサポート（環境変数が優先）：

```json
{
  "api_base_url": "https://ai.6551.io/news-platform",
  "wss_url": "wss://ai.6551.io/news-platform/rpc",
  "api_token": "your-api-token-here",
  "max_rows": 100
}
```

---

## データ構造

各記事：

```json
{
  "id": "unique-article-id",
  "text": "タイトル / 内容",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [{ "symbol": "BTC", "market_type": "spot", "match": "title" }],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long",
    "status": "done",
    "summary": "中国語の要約",
    "enSummary": "English summary"
  },
  "ts": 1708473600000
}
```

| AI フィールド | 説明 |
|-------------|------|
| `score` | 0-100 影響度評価 |
| `signal` | `long`（強気）/ `short`（弱気）/ `neutral` |
| `status` | `done` = AI 分析完了 |

---

<details>
<summary><b>その他のクライアント — 手動インストール</b>（クリックで展開）</summary>

> 以下のすべての設定で `/path/to/opennews-mcp` をローカルの実際のプロジェクトパスに置き換えてください。`OPENNEWS_TOKEN` の値は上記の無料トライアル Token を使用できます。

### Claude Desktop

設定ファイルを編集（macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`、Windows: `%APPDATA%\Claude\claude_desktop_config.json`）：

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

`~/.cursor/mcp.json` または Settings > MCP Servers：

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

`~/.codeium/windsurf/mcp_config.json`：

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

VS Code サイドバー > Cline > MCP Servers > Configure、`cline_mcp_settings.json` を編集：

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
      OPENNEWS_TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c
```

### Cherry Studio

設定 > MCP サーバー > 追加 > タイプ stdio：Command `uv`、Args `--directory /path/to/opennews-mcp run opennews-mcp`、Env `OPENNEWS_TOKEN`。

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
          "OPENNEWS_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c"
        }
      }
    }
  }
}
```

### 任意の stdio MCP クライアント

```bash
OPENNEWS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiNjU1MW5ld3NtY3AiLCJ1c2VybmFtZSI6IjY1NTFuZXdzbWNwIn0.namttZDCVLOIlEGwIkJPBrcV-foaXQgqibDcmpck02c \
  uv --directory /path/to/opennews-mcp run opennews-mcp
```

</details>

---

## 互換性

| クライアント | インストール方法 | ステータス |
|-------------|-----------------|-----------|
| **Claude Code** | `claude mcp add` | ワンライナー |
| **OpenClaw** | Skill ディレクトリコピー | ワンライナー |
| Claude Desktop | JSON 設定 | 対応 |
| Cursor | JSON 設定 | 対応 |
| Windsurf | JSON 設定 | 対応 |
| Cline | JSON 設定 | 対応 |
| Continue.dev | YAML / JSON | 対応 |
| Cherry Studio | GUI | 対応 |
| Zed | JSON 設定 | 対応 |

---

## 関連プロジェクト

- [twitter-mcp](https://github.com/6551-io/twitter-mcp) - Twitter/X データ MCP サーバー

---

## 開発

```bash
cd /path/to/opennews-mcp
uv sync
uv run opennews-mcp
```

```bash
# MCP Inspector
npx @modelcontextprotocol/inspector uv --directory /path/to/opennews-mcp run opennews-mcp
```

### プロジェクト構造

```
├── README.md                  # 中文（デフォルト）
├── docs/
│   ├── README_EN.md           # English
│   ├── README_JA.md           # 日本語
│   └── README_KO.md           # 한국어
├── openclaw-skill/opennews/   # OpenClaw Skill
├── knowledge/guide.md         # 組み込みナレッジ
├── pyproject.toml
├── config.json
└── src/opennews_mcp/
    ├── server.py              # エントリポイント
    ├── app.py                 # FastMCP インスタンス
    ├── config.py              # 設定ローダー
    ├── api_client.py          # HTTP + WebSocket
    └── tools/                 # 11 ツール
```

## ライセンス

MIT
