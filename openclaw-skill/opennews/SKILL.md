---
name: opennews
description: Crypto news search, AI ratings, trading signals, and real-time updates via the OpenNews 6551 API. Supports keyword search, coin filtering, source filtering, date range queries, AI score ranking, and WebSocket live feeds.

user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - OPENNEWS_TOKEN
      bins:
        - curl
    primaryEnv: OPENNEWS_TOKEN
    emoji: "\U0001F4F0"
    install:
      - id: curl
        kind: brew
        formula: curl
        label: curl (HTTP client)
    os:
      - darwin
      - linux
      - win32
---

# OpenNews Crypto News Skill

Query crypto news from the 6551 news platform REST API. All endpoints require a Bearer token via `$OPENNEWS_TOKEN`.

**Base URL**: `https://ai.6551.io/news-platform`

## Authentication

All requests require the header:
```
Authorization: Bearer $OPENNEWS_TOKEN
```

## Available Operations

### 1. Get News Sources

Fetch all available news source categories organized by engine type.

```bash
curl -s -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  "https://ai.6551.io/news-platform/v1/engine/tree"
```

Returns a tree with engine types (`news`, `listing`, `onchain`, `meme`, `market`) and their sub-categories (Bloomberg, Reuters, Binance, etc.). Each category has `code`, `name`, `enName`, and `aiEnabled` fields.

Use this first to discover available `newsType` codes for filtering.

### 2. Search News (Primary Endpoint)

`POST /v1/news/search` is the single search endpoint. All filtering is done via JSON body parameters.

**Get latest news (no filter):**
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}'
```

**Search by keyword:**
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "bitcoin ETF", "limit": 10, "page": 1}'
```

**Search by coin symbol:**
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC"], "limit": 10, "page": 1}'
```

Multiple coins: `"coins": ["BTC", "ETH", "SOL"]`

**Filter by news source:**
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"newsType": "Bloomberg", "limit": 10, "page": 1}'
```

Common sources: `Bloomberg`, `Reuters`, `Coindesk`, `CoinTelegraph`, `TheBlock`.

**Filter by engine type:**
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"engineType": "news", "limit": 10, "page": 1}'
```

Engine types: `news`, `listing`, `onchain`, `meme`, `market`.

**Search within date range:**
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startDate": 1708387200000, "endDate": 1708473600000, "limit": 20, "page": 1}'
```

Dates are Unix timestamps in **milliseconds**. You can combine with `coins`, `query`, `newsType`, and `engineType`.

**Combined filters example:**
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC"], "query": "SEC", "engineType": "news", "limit": 20, "page": 1}'
```

### 3. POST Body Parameters Reference

| Parameter    | Type       | Required | Description                                   |
|-------------|------------|----------|-----------------------------------------------|
| `limit`     | integer    | yes      | Max results per page (1-100)                  |
| `page`      | integer    | yes      | Page number (1-based)                         |
| `query`     | string     | no       | Full-text keyword search                      |
| `coins`     | string[]   | no       | Filter by coin symbols (e.g. `["BTC","ETH"]`) |
| `newsType`  | string     | no       | Filter by source code (e.g. `"Bloomberg"`)    |
| `engineType`| string     | no       | Filter by engine (`news`,`listing`,`onchain`,`meme`,`market`) |
| `startDate` | integer    | no       | Start timestamp in milliseconds               |
| `endDate`   | integer    | no       | End timestamp in milliseconds                 |

## Article Data Structure

Each article in the `data` array contains:

```json
{
  "id": "unique-article-id",
  "text": "Article headline / content text",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://original-article-url.com/...",
  "coins": [
    {"symbol": "BTC", "market_type": "spot", "match": "title"}
  ],
  "aiRating": {
    "score": 85,
    "grade": "A",
    "signal": "long",
    "status": "done",
    "summary": "Chinese summary text",
    "enSummary": "English summary text"
  },
  "ts": 1708473600000
}
```

### AI Rating Fields

- `score`: 0-100 numeric rating (higher = more impactful)
- `grade`: Letter grade (A/B/C/D)
- `signal`: Trading signal — `"long"` (bullish), `"short"` (bearish), or `"neutral"`
- `status`: `"done"` when AI analysis is complete
- `summary` / `enSummary`: AI-generated summary in Chinese / English

## Common Workflows

### Quick Market Overview
Fetch latest 10 news articles:
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}' | jq '.data[] | {text, newsType, signal: .aiRating.signal, score: .aiRating.score}'
```

### High-Impact News
Fetch articles and filter for AI score >= 80:
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 50, "page": 1}' | jq '[.data[] | select(.aiRating.score >= 80)] | sort_by(-.aiRating.score)'
```

### Bullish Signals Only
Filter articles with `"long"` trading signal:
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 50, "page": 1}' | jq '[.data[] | select(.aiRating.signal == "long" and .aiRating.status == "done")]'
```

### Coin-Specific Research
Get BTC-related news from the last 24 hours:
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"coins\": [\"BTC\"], \"startDate\": $(date -d '24 hours ago' +%s)000, \"limit\": 20, \"page\": 1}"
```

### Source-Specific Feed
Get Bloomberg articles about ETH:
```bash
curl -s -X POST "https://ai.6551.io/news-platform/v1/news/search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["ETH"], "newsType": "Bloomberg", "limit": 10, "page": 1}'
```

## Response Format

All search responses follow this structure:
```json
{
  "code": 0,
  "data": [ ... articles ... ],
  "total": 1234,
  "page": 1,
  "limit": 10
}
```

- `code`: 0 = success
- `data`: Array of article objects
- `total`: Total matching articles available
- `page` / `limit`: Current pagination state

## Notes

- Rate limits apply; avoid requesting more than 100 articles per call.
- AI ratings (`aiRating`) may not be available on all articles. Check `status == "done"` before using `score` or `signal`.
- The `coins` array in articles shows which coins were detected and where the match occurred (`title`, `content`).
- Timestamps (`ts`, `startDate`, `endDate`) are in Unix milliseconds.
- Use `get /v1/engine/tree` first to discover all valid `newsType` and `engineType` values.
