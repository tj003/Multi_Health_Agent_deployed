from __future__ import annotations
import httpx
import asyncio
import feedparser
import logging
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from httpx import HTTPStatusError
from ..config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class FetchError(Exception):
    pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, max=8),
    reraise=True,
    retry=retry_if_exception_type(FetchError),
)
async def _get(client: httpx.AsyncClient, url: str) -> bytes:
    try:
        r = await client.get(url, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.content
    except HTTPStatusError as e:
        if 400 <= e.response.status_code < 500:
            logger.error(f" Permanent {e.response.status_code} for {url}")
            raise Exception(f"{e.response.status_code} {url}") 
        raise FetchError(str(e))
    except Exception as e:
        logger.warning(f" Transient fetch failed: {url} | {e}")
        raise FetchError(str(e))

async def fetch_feeds(feed_urls: List[str], max_items: int = 5) -> List[Dict]:
    """Fetch multiple RSS feeds concurrently and return parsed items."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [_get(client, u) for u in feed_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    items: List[Dict] = []
    seen = set()

    for content, url in zip(results, feed_urls):
        if isinstance(content, Exception):
            logger.error(f"Skipping feed due to error: {url} | {content}")
            continue
        try:
            parsed = feedparser.parse(content)
            for entry in parsed.entries[:max_items]:
                key = (entry.get("title", ""), entry.get("link", ""))
                if key in seen:
                    continue
                seen.add(key)
                items.append({
                    "title": entry.get("title", "No Title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", entry.get("updated", "N/A")),
                    "source": url,
                })
        except Exception as e:
            logger.error(f"Parse error for {url}: {e}")
    return items
