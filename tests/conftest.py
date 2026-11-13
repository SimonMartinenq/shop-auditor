from collections.abc import Iterator

import pytest
from fixture_server import serve_shops


@pytest.fixture(scope="session")
def shop_urls() -> Iterator[dict[str, str]]:
    """Base URL of each fixture shop, served for the whole test session."""
    with serve_shops() as urls:
        yield urls
