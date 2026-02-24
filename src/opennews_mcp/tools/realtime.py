"""Real-time news tools — WebSocket subscription for live news updates."""

from mcp.server.fastmcp import Context

from opennews_mcp.app import mcp
from opennews_mcp.config import make_serializable


@mcp.tool()
async def subscribe_latest_news(ctx: Context, wait_seconds: int = 10, max_items: int = 5) -> dict:
    """Subscribe to real-time news updates via WebSocket.

    Connects to the WebSocket feed, subscribes to latest news, and collects
    incoming messages for the specified duration.

    Args:
        wait_seconds: How long to listen for news (default 10, max 30 seconds).
        max_items: Maximum news items to collect (default 5, max 20).
    """
    ws = ctx.request_context.lifespan_context.ws
    wait_seconds = min(max(1, wait_seconds), 30)
    max_items = min(max(1, max_items), 20)

    try:
        sub_result = await ws.subscribe_latest()

        items = []
        for _ in range(max_items):
            msg = await ws.receive_news(timeout=float(wait_seconds))
            if msg is None:
                break
            items.append(msg)

        return make_serializable({
            "success": True,
            "data": items,
            "count": len(items),
        })
    except Exception as e:
        return {"success": False, "error": str(e) or repr(e)}
    finally:
        await ws.close()
