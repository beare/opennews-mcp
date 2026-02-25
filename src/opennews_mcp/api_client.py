"""HTTP/WebSocket client for the 6551 news platform API."""

import asyncio
import json
import time
import logging
from typing import Any, Optional

import httpx

from opennews_mcp.config import API_BASE_URL, WSS_URL, API_TOKEN

logger = logging.getLogger(__name__)

MAX_RETRIES = 2


class NewsAPIClient:
    """Async HTTP client for the 6551 news REST API."""

    def __init__(self, base_url: str = API_BASE_URL, token: str = API_TOKEN):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._client: Optional[httpx.AsyncClient] = None

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                headers=self._headers(),
            )
        return self._client

    async def _reset_client(self):
        """Force close and recreate the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
        self._client = None

    async def close(self):
        await self._reset_client()

    # ---------- internal request with retry ----------

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Execute an HTTP request with automatic retry on connection errors."""
        last_exc = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                client = await self._get_client()
                resp = await client.request(method, url, **kwargs)
                resp.raise_for_status()
                return resp
            except (httpx.ConnectError, httpx.RemoteProtocolError) as e:
                last_exc = e
                logger.warning(
                    "Connection error (attempt %d/%d): %s",
                    attempt + 1, MAX_RETRIES + 1, repr(e),
                )
                await self._reset_client()
            except httpx.HTTPStatusError:
                raise
        raise last_exc  # type: ignore[misc]

    # ---------- REST endpoints ----------

    async def get_engine_tree(self) -> dict:
        """GET /open/news_type — 获取所有新闻源分类"""
        resp = await self._request("GET", f"{self.base_url}/open/news_type")
        return resp.json()

    async def search_news(
        self,
        coins: Optional[list[str]] = None,
        query: Optional[str] = None,
        engine_types: Optional[dict[str, list[str]]] = None,
        has_coin: bool = False,
        limit: int = 20,
        page: int = 1,
    ) -> dict:
        """POST /open/news_search — 搜索新闻文章"""
        body: dict[str, Any] = {"limit": limit, "page": page}
        if coins:
            body["coins"] = coins
        if query:
            body["q"] = query
        if engine_types:
            body["engineTypes"] = engine_types
        if has_coin:
            body["hasCoin"] = has_coin

        resp = await self._request("POST", f"{self.base_url}/open/news_search", json=body)
        return resp.json()

    # ---------- Twitter endpoints ----------

    async def get_twitter_user_info(self, username: str) -> dict:
        """POST /open/twitter_user_info — 获取Twitter用户信息（通过用户名）"""
        resp = await self._request("POST", f"{self.base_url}/open/twitter_user_info", json={"username": username})
        return resp.json()

    async def get_twitter_user_by_id(self, user_id: str) -> dict:
        """POST /open/twitter_user_by_id — 获取Twitter用户信息（通过ID）"""
        resp = await self._request("POST", f"{self.base_url}/open/twitter_user_by_id", json={"userId": user_id})
        return resp.json()

    async def get_twitter_user_tweets(
        self,
        username: str,
        max_results: int = 20,
        product: str = "Latest",
        include_replies: bool = False,
        include_retweets: bool = False,
    ) -> dict:
        """POST /open/twitter_user_tweets — 获取用户推文"""
        body = {
            "username": username,
            "maxResults": max_results,
            "product": product,
            "includeReplies": include_replies,
            "includeRetweets": include_retweets,
        }
        resp = await self._request("POST", f"{self.base_url}/open/twitter_user_tweets", json=body)
        return resp.json()

    async def search_twitter(
        self,
        keywords: Optional[str] = None,
        from_user: Optional[str] = None,
        to_user: Optional[str] = None,
        mention_user: Optional[str] = None,
        hashtag: Optional[str] = None,
        exclude_replies: bool = False,
        exclude_retweets: bool = False,
        min_likes: int = 0,
        min_retweets: int = 0,
        min_replies: int = 0,
        since_date: Optional[str] = None,
        until_date: Optional[str] = None,
        lang: Optional[str] = None,
        product: str = "Top",
        max_results: int = 20,
    ) -> dict:
        """POST /open/twitter_search — Twitter搜索"""
        body: dict[str, Any] = {
            "maxResults": max_results,
            "product": product,
        }
        if keywords:
            body["keywords"] = keywords
        if from_user:
            body["fromUser"] = from_user
        if to_user:
            body["toUser"] = to_user
        if mention_user:
            body["mentionUser"] = mention_user
        if hashtag:
            body["hashtag"] = hashtag
        if exclude_replies:
            body["excludeReplies"] = exclude_replies
        if exclude_retweets:
            body["excludeRetweets"] = exclude_retweets
        if min_likes > 0:
            body["minLikes"] = min_likes
        if min_retweets > 0:
            body["minRetweets"] = min_retweets
        if min_replies > 0:
            body["minReplies"] = min_replies
        if since_date:
            body["sinceDate"] = since_date
        if until_date:
            body["untilDate"] = until_date
        if lang:
            body["lang"] = lang

        resp = await self._request("POST", f"{self.base_url}/open/twitter_search", json=body)
        return resp.json()

    async def get_twitter_follower_events(
        self,
        username: str,
        is_follow: bool = True,
        max_results: int = 20,
    ) -> dict:
        """POST /open/twitter_follower_events — 获取关注/取关事件"""
        body = {
            "username": username,
            "isFollow": is_follow,
            "maxResults": max_results,
        }
        resp = await self._request("POST", f"{self.base_url}/open/twitter_follower_events", json=body)
        return resp.json()

    async def get_twitter_deleted_tweets(
        self,
        username: str,
        max_results: int = 20,
    ) -> dict:
        """POST /open/twitter_deleted_tweets — 获取删推数据"""
        body = {
            "username": username,
            "maxResults": max_results,
        }
        resp = await self._request("POST", f"{self.base_url}/open/twitter_deleted_tweets", json=body)
        return resp.json()

    async def get_twitter_kol_followers(self, username: str) -> dict:
        """POST /open/twitter_kol_followers — 获取大V关注者"""
        resp = await self._request("POST", f"{self.base_url}/open/twitter_kol_followers", json={"username": username})
        return resp.json()


class NewsWSClient:
    """WebSocket client for real-time news subscription."""

    def __init__(self, wss_url: str = WSS_URL, token: str = API_TOKEN):
        self.wss_url = f"{wss_url}?token={token}"
        self._ws = None
        self._request_id = 0

    def _next_id(self) -> str:
        self._request_id += 1
        return f"req_{self._request_id}_{int(time.time())}"

    async def connect(self):
        import websockets
        self._ws = await websockets.connect(self.wss_url)

    async def close(self):
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def subscribe_latest(
        self,
        engine_types: Optional[dict[str, list[str]]] = None,
        coins: Optional[list[str]] = None,
        has_coin: bool = False,
    ) -> dict:
        """订阅新闻推送，支持过滤器"""
        if not self._ws:
            await self.connect()
        req_id = self._next_id()
        params: dict[str, Any] = {}
        if engine_types:
            params["engineTypes"] = engine_types
        if coins:
            params["coins"] = coins
        if has_coin:
            params["hasCoin"] = has_coin
        msg = {"method": "news.subscribe", "id": req_id, "params": params}
        await self._ws.send(json.dumps(msg))
        resp = await self._ws.recv()
        return json.loads(resp)

    async def receive_news(self, timeout: float = 10.0) -> Optional[dict]:
        if not self._ws:
            return None
        try:
            msg = await asyncio.wait_for(self._ws.recv(), timeout=timeout)
            return json.loads(msg)
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            logger.warning("WebSocket receive error: %s", repr(e))
            return None
