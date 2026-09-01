#!/usr/bin/env python3
"""
🌐 Sofi Web MCP Server — جلب صفحات الويب وتحويلها لنص
=======================================================
JSON-RPC 2.0 stdio MCP server: fetch a URL and return clean text/markdown.
Stdlib-only (urllib + html.parser) — لا يحتاج أي تثبيت خارجي.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.mcp.base import SofiBaseMCP
import json
import re
import gzip
import urllib.request
import urllib.error
from html.parser import HTMLParser
from typing import Dict, List


TOOLS = [
    {
        "name": "fetch",
        "description": "جلب صفحة ويب وتحويلها لنص نظيف — Fetch a URL and return clean readable text (HTML stripped to markdown-ish text).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to fetch (http/https)"},
                "max_length": {"type": "integer", "description": "Max characters to return", "default": 8000},
                "start_index": {"type": "integer", "description": "Character offset to start from (for pagination)", "default": 0},
                "raw": {"type": "boolean", "description": "Return raw HTML instead of cleaned text", "default": False}
            },
            "required": ["url"]
        }
    },
    {
        "name": "fetch_links",
        "description": "استخراج كل الروابط من صفحة — Extract all hyperlinks (href + anchor text) from a page.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to extract links from"},
                "limit": {"type": "integer", "description": "Max links to return", "default": 50}
            },
            "required": ["url"]
        }
    }
]

_UA = "Mozilla/5.0 (compatible; SofiWebMCP/1.0; +https://sofi.ai)"
_SKIP_TAGS = {"script", "style", "head", "noscript", "svg", "iframe", "template"}
_BLOCK_TAGS = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
               "section", "article", "header", "footer", "ul", "ol", "table", "pre"}


class _TextExtractor(HTMLParser):
    """يحوّل HTML إلى نص مع الحفاظ على فواصل الأسطر للعناصر الكتلية."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: List[str] = []
        self._skip_depth = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "a":
            href = dict(attrs).get("href")
            if href and href.startswith(("http://", "https://")):
                self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False
        if tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip_depth > 0:
            return
        if self._in_title:
            self.title += data
        text = data.strip()
        if text:
            self.parts.append(text)

    def get_text(self) -> str:
        raw = " ".join(self.parts)
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n[ \t]+", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


class _LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: List[Dict] = []
        self._cur_href = None
        self._cur_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self._cur_href = href
                self._cur_text = []

    def handle_data(self, data):
        if self._cur_href is not None:
            t = data.strip()
            if t:
                self._cur_text.append(t)

    def handle_endtag(self, tag):
        if tag == "a" and self._cur_href is not None:
            self.links.append({"href": self._cur_href, "text": " ".join(self._cur_text)[:120]})
            self._cur_href = None


def _http_get(url: str, timeout: int = 20) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
        charset = resp.headers.get_content_charset() or "utf-8"
        return data.decode(charset, errors="replace")


class WebMCPServer(SofiBaseMCP):
    def __init__(self):
        super().__init__("🌐 Web MCP", "1.0.0", TOOLS)

    async def handle_tool_call(self, name: str, arguments: Dict) -> Dict:
        try:
            if name == "fetch":
                return await self._fetch(arguments)
            elif name == "fetch_links":
                return await self._fetch_links(arguments)
            return self._text_error(f"أداة غير معروفة: {name}")
        except urllib.error.HTTPError as e:
            return self._text_error(f"HTTP {e.code}: {e.reason} — {arguments.get('url')}")
        except urllib.error.URLError as e:
            return self._text_error(f"URL error: {e.reason} — {arguments.get('url')}")
        except Exception as e:
            return self._text_error(f"{type(e).__name__}: {e}")

    async def _fetch(self, args: Dict) -> Dict:
        url = args.get("url", "")
        if not url:
            return self._text_error("الوسيط 'url' مطلوب")
        max_length = int(args.get("max_length", 8000))
        start = int(args.get("start_index", 0))
        raw = bool(args.get("raw", False))
        html = await asyncio.to_thread(_http_get, url)
        if raw:
            body = html
            header = f"# RAW {url}\n\n"
        else:
            parser = _TextExtractor()
            parser.feed(html)
            text = parser.get_text()
            header = f"# {parser.title.strip() or url}\nURL: {url}\n\n"
            body = text
        chunk = body[start:start + max_length]
        more = ""
        if start + max_length < len(body):
            more = f"\n\n… [مقتطع — استخدم start_index={start + max_length} للمزيد | total {len(body)} chars]"
        return self._text_result(header + chunk + more)

    async def _fetch_links(self, args: Dict) -> Dict:
        url = args.get("url", "")
        if not url:
            return self._text_error("الوسيط 'url' مطلوب")
        limit = int(args.get("limit", 50))
        html = await asyncio.to_thread(_http_get, url)
        parser = _LinkExtractor()
        parser.feed(html)
        links = parser.links[:limit]
        return self._text_result(json.dumps({"url": url, "count": len(links), "links": links},
                                            ensure_ascii=False, indent=2))


if __name__ == "__main__":
    server = WebMCPServer()
    asyncio.run(server.run())
