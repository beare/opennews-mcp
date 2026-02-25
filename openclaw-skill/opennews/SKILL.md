---
name: opennews
description: Crypto news search, AI ratings, trading signals, real-time updates, and Twitter/X data via the OpenNews 6551 API. Supports keyword search, coin filtering, source filtering, AI score ranking, WebSocket live feeds, Twitter user profiles, and tweet search.

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

# OpenNews Crypto News & Twitter Skill

Query crypto news and Twitter data from the 6551 platform REST API. All endpoints require a Bearer token via `$OPENNEWS_TOKEN`.

**Get your token**: https://6551.io/mcp

**Base URL**: `https://ai.6551.io`

## Authentication

All requests require the header:
```
Authorization: Bearer $OPENNEWS_TOKEN
```

---

## News Operations

### 1. Get News Sources

Fetch all available news source categories organized by engine type.

```bash
curl -s -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  "https://ai.6551.io/open/news_type"
```

Returns a tree with engine types (`news`, `listing`, `onchain`, `meme`, `market`) and their sub-categories.

### 2. Search News

`POST /open/news_search` is the primary search endpoint.

**Get latest news:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}'
```

**Search by keyword:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"q": "bitcoin ETF", "limit": 10, "page": 1}'
```

**Search by coin symbol:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"coins": ["BTC"], "limit": 10, "page": 1}'
```

**Filter by engine type and news type:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"engineTypes": {"news": ["Bloomberg", "Reuters"]}, "limit": 10, "page": 1}'
```

**Only news with coins:**
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hasCoin": true, "limit": 10, "page": 1}'
```

### News Search Parameters

| Parameter     | Type                      | Required | Description                                   |
|--------------|---------------------------|----------|-----------------------------------------------|
| `limit`      | integer                   | yes      | Max results per page (1-100)                  |
| `page`       | integer                   | yes      | Page number (1-based)                         |
| `q`          | string                    | no       | Full-text keyword search                      |
| `coins`      | string[]                  | no       | Filter by coin symbols (e.g. `["BTC","ETH"]`) |
| `engineTypes`| map[string][]string       | no       | Filter by engine and news types               |
| `hasCoin`    | boolean                   | no       | Only return news with associated coins        |

---

## Twitter Operations

### 1. Get Twitter User Info

Get user profile by username.

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_info" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk"}'
```

### 2. Get Twitter User by ID

Get user profile by numeric ID.

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_by_id" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"userId": "44196397"}'
```

### 3. Get User Tweets

Get recent tweets from a user.

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_tweets" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "elonmusk", "maxResults": 20, "product": "Latest"}'
```

| Parameter         | Type    | Default  | Description                    |
|------------------|---------|----------|--------------------------------|
| `username`       | string  | required | Twitter username (without @)   |
| `maxResults`     | integer | 20       | Max tweets (1-100)             |
| `product`        | string  | "Latest" | "Latest" or "Top"              |
| `includeReplies` | boolean | false    | Include reply tweets           |
| `includeRetweets`| boolean | false    | Include retweets               |

### 4. Search Twitter

Search tweets with various filters.

```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": "bitcoin", "maxResults": 20, "product": "Top"}'
```

**Search from specific user:**
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fromUser": "VitalikButerin", "maxResults": 20}'
```

**Search by hashtag:**
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hashtag": "crypto", "minLikes": 100, "maxResults": 20}'
```

### Twitter Search Parameters

| Parameter         | Type    | Default | Description                         |
|------------------|---------|---------|-------------------------------------|
| `keywords`       | string  | -       | Search keywords                     |
| `fromUser`       | string  | -       | Tweets from specific user           |
| `toUser`         | string  | -       | Tweets to specific user             |
| `mentionUser`    | string  | -       | Tweets mentioning user              |
| `hashtag`        | string  | -       | Filter by hashtag (without #)       |
| `excludeReplies` | boolean | false   | Exclude reply tweets                |
| `excludeRetweets`| boolean | false   | Exclude retweets                    |
| `minLikes`       | integer | 0       | Minimum likes threshold             |
| `minRetweets`    | integer | 0       | Minimum retweets threshold          |
| `minReplies`     | integer | 0       | Minimum replies threshold           |
| `sinceDate`      | string  | -       | Start date (YYYY-MM-DD)             |
| `untilDate`      | string  | -       | End date (YYYY-MM-DD)               |
| `lang`           | string  | -       | Language code (e.g. "en", "zh")     |
| `product`        | string  | "Top"   | "Top" or "Latest"                   |
| `maxResults`     | integer | 20      | Max tweets (1-100)                  |

---

## Data Structures

### News Article

```json
{
  "id": "unique-article-id",
  "text": "Article headline / content",
  "newsType": "Bloomberg",
  "engineType": "news",
  "link": "https://...",
  "coins": [{"symbol": "BTC", "market_type": "spot", "match": "title"}],
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

### Twitter User

```json
{
  "userId": "44196397",
  "screenName": "elonmusk",
  "name": "Elon Musk",
  "description": "...",
  "followersCount": 170000000,
  "friendsCount": 500,
  "statusesCount": 30000,
  "verified": true
}
```

### Tweet

```json
{
  "id": "1234567890",
  "text": "Tweet content...",
  "createdAt": "2024-02-20T12:00:00Z",
  "retweetCount": 1000,
  "favoriteCount": 5000,
  "replyCount": 200,
  "userScreenName": "elonmusk",
  "hashtags": ["crypto", "bitcoin"],
  "urls": [{"url": "https://..."}]
}
```

---

## Common Workflows

### Quick Market Overview
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 1}' | jq '.data[] | {text, newsType, signal: .aiRating.signal}'
```

### High-Impact News (score >= 80)
```bash
curl -s -X POST "https://ai.6551.io/open/news_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"limit": 50, "page": 1}' | jq '[.data[] | select(.aiRating.score >= 80)]'
```

### Crypto Twitter KOL Tweets
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_user_tweets" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username": "VitalikButerin", "maxResults": 10}'
```

### Trending Crypto Tweets
```bash
curl -s -X POST "https://ai.6551.io/open/twitter_search" \
  -H "Authorization: Bearer $OPENNEWS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keywords": "bitcoin", "minLikes": 1000, "product": "Top", "maxResults": 20}'
```

## Notes

- Get your API token at https://6551.io/mcp
- Rate limits apply; max 100 results per request
- AI ratings may not be available on all articles (check `status == "done"`)
- Twitter usernames should not include the @ symbol
