"""Serve the fixture shops locally, each on its own port (= its own origin).

Manual use: `uv run python tests/fixture_server.py`, then open the printed URLs.
"""

import random
import struct
import threading
import zlib
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict

from shop_auditor.models import Axis, PageType, Platform, Severity

SITES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "sites"

PAGE_PATHS = {
    PageType.HOME: "/",
    PageType.COLLECTION: "/collection.html",
    PageType.PRODUCT: "/product.html",
    PageType.CART: "/cart.html",
    PageType.CONTENT: "/about.html",
}


class ExpectedDefect(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    axis: Axis
    severity: Severity
    pages: list[PageType]
    description: str
    lighthouse_detects: bool  # feeds the "value added vs Lighthouse" eval


class ExpectedShop(BaseModel):
    model_config = ConfigDict(extra="forbid")
    port: int
    platform: Platform
    defects: list[ExpectedDefect]


def load_expected() -> dict[str, ExpectedShop]:
    return {
        path.parent.name: ExpectedShop.model_validate(yaml.safe_load(path.read_text()))
        for path in sorted(SITES_DIR.glob("*/expected.yaml"))
    }


def write_noise_png(path: Path, width: int = 1400, height: int = 1000) -> None:
    """Random pixels don't compress: a ~4 MB PNG without committing it to git."""
    rng = random.Random(0)
    raw = b"".join(b"\x00" + rng.randbytes(width * 3) for _ in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        )

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 1))
        + chunk(b"IEND", b"")
    )


def ensure_generated_assets() -> None:
    hero = SITES_DIR / "slow" / "img" / "hero.png"
    if not hero.exists():
        write_noise_png(hero)


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        pass


@contextmanager
def serve_shops() -> Iterator[dict[str, str]]:
    """Start one HTTP server per shop; yield {shop name: base URL}."""
    ensure_generated_assets()
    servers = []
    urls = {}
    try:
        for name, shop in load_expected().items():
            handler = partial(_QuietHandler, directory=str(SITES_DIR / name))
            server = ThreadingHTTPServer(("127.0.0.1", shop.port), handler)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            servers.append(server)
            urls[name] = f"http://127.0.0.1:{shop.port}"
        yield urls
    finally:
        for server in servers:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    with serve_shops() as shop_urls:
        for shop_name, url in shop_urls.items():
            print(f"{shop_name:10} {url}")
        print("Ctrl+C pour arrêter.")
        with suppress(KeyboardInterrupt):
            threading.Event().wait()
