"""News content tools — search and retrieve crypto news via REST API.

Uses POST /v1/news/search as the primary data source.
Returns raw article data as-is from the API.
"""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import clamp_limit, make_serializable, MAX_ROWS


@mcp.tool()
async def get_latest_news(ctx: Context, limit: int = 10) -> dict:
    """Get the most recent crypto news articles, newest first.

    Returns news with title text, source, link, related coins, AI rating, and tags.

    Args:
        limit: Maximum number of articles to return (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def search_news(keyword: str, ctx: Context, limit: int = 10) -> dict:
    """Search crypto news by keyword in text content.

    Args:
        keyword: Search term (e.g. "bitcoin", "SEC", "ETF").
        limit: Maximum results (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(query=keyword, limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "keyword": keyword, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def search_news_by_coin(coin: str, ctx: Context, limit: int = 10) -> dict:
    """Search news related to a specific cryptocurrency coin/token.

    Args:
        coin: Coin symbol or name (e.g. "BTC", "ETH", "SOL", "TRUMP").
        limit: Maximum results (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(coins=[coin], limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "coin": coin, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_news_by_source(source: str, ctx: Context, limit: int = 10) -> dict:
    """Get news articles from a specific source.

    Use list_news_types first to see available source codes.

    Args:
        source: The news source code (e.g. "Bloomberg", "Reuters", "Coindesk").
        limit: Maximum results (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(news_type=source, limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "source": source, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_news_by_engine(engine_type: str, ctx: Context, limit: int = 10) -> dict:
    """Get news articles filtered by engine type.

    Engine types: "news", "listing", "onchain", "meme", "market".

    Args:
        engine_type: The engine type code.
        limit: Maximum results (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        result = await api.search_news(engine_type=engine_type, limit=limit, page=1)
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "engine_type": engine_type, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def search_news_by_date(
    ctx: Context,
    start_date: str = "",
    end_date: str = "",
    coins: str = "",
    keyword: str = "",
    limit: int = 10,
) -> dict:
    """Search news within a date range.

    Args:
        start_date: Start date as ISO string (e.g. "2026-02-20") or unix timestamp in ms.
        end_date: End date as ISO string (e.g. "2026-02-23") or unix timestamp in ms.
        coins: Comma-separated coin symbols (e.g. "BTC,ETH").
        keyword: Optional search keyword.
        limit: Maximum results (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)

    start_ts = None
    end_ts = None
    if start_date:
        try:
            start_ts = int(start_date)
        except ValueError:
            from datetime import datetime
            dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            start_ts = int(dt.timestamp() * 1000)
    if end_date:
        try:
            end_ts = int(end_date)
        except ValueError:
            from datetime import datetime
            dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            end_ts = int(dt.timestamp() * 1000)

    coin_list = [c.strip() for c in coins.split(",") if c.strip()] if coins else None

    try:
        result = await api.search_news(
            coins=coin_list, query=keyword or None,
            limit=limit, page=1,
            start_date=start_ts, end_date=end_ts,
        )
        data = result.get("data", [])[:limit]
        return make_serializable({
            "success": True, "data": data,
            "count": len(data), "total": result.get("total", 0),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_high_score_news(ctx: Context, min_score: int = 70, limit: int = 10) -> dict:
    """Get highly-rated news articles (by AI score), sorted by score descending.

    Args:
        min_score: Minimum score threshold (default 70).
        limit: Maximum results to return (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        fetch_limit = min(limit * 3, MAX_ROWS)
        result = await api.search_news(limit=fetch_limit, page=1)
        raw = result.get("data", [])

        filtered = [it for it in raw
                     if (it.get("aiRating") or {}).get("score", 0) >= min_score]
        filtered.sort(
            key=lambda x: (x.get("aiRating") or {}).get("score", 0),
            reverse=True,
        )
        data = filtered[:limit]
        return make_serializable({
            "success": True, "min_score": min_score,
            "data": data, "count": len(data),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}


@mcp.tool()
async def get_news_by_signal(signal: str, ctx: Context, limit: int = 10) -> dict:
    """Get news filtered by trading signal type.

    Args:
        signal: The signal type: "long" (bullish), "short" (bearish), or "neutral".
        limit: Maximum results (default 10, max 100).
    """
    api = ctx.request_context.lifespan_context.api
    limit = clamp_limit(limit)
    try:
        fetch_limit = min(limit * 3, MAX_ROWS)
        result = await api.search_news(limit=fetch_limit, page=1)
        raw = result.get("data", [])

        filtered = [it for it in raw
                     if (it.get("aiRating") or {}).get("signal") == signal
                     and (it.get("aiRating") or {}).get("status") == "done"]
        data = filtered[:limit]
        return make_serializable({
            "success": True, "signal": signal,
            "data": data, "count": len(data),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}
