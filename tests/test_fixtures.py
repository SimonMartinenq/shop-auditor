"""The fixture shops are served correctly and their expected.yaml files are coherent."""

from urllib.error import HTTPError
from urllib.request import urlopen

import pytest
from fixture_server import PAGE_PATHS, SITES_DIR, load_expected

EXPECTED = load_expected()


def test_every_shop_has_an_expected_file() -> None:
    shops = {p.name for p in SITES_DIR.iterdir() if p.is_dir()}
    assert shops == set(EXPECTED)


def test_clean_shop_is_the_only_one_without_defects() -> None:
    assert [name for name, shop in EXPECTED.items() if not shop.defects] == ["clean"]


def test_defect_ids_are_unique() -> None:
    ids = [d.id for shop in EXPECTED.values() for d in shop.defects]
    assert len(ids) == len(set(ids))


def test_ports_are_unique() -> None:
    ports = [shop.port for shop in EXPECTED.values()]
    assert len(ports) == len(set(ports))


@pytest.mark.parametrize("shop", sorted(EXPECTED))
def test_every_page_is_served(shop_urls: dict[str, str], shop: str) -> None:
    for path in [*PAGE_PATHS.values(), "/robots.txt"]:
        with urlopen(shop_urls[shop] + path) as response:
            assert response.status == 200, path


def test_planted_heavy_hero_is_about_4mb(shop_urls: dict[str, str]) -> None:
    with urlopen(shop_urls["slow"] + "/img/hero.png") as response:
        assert 3_500_000 < len(response.read()) < 5_000_000


def test_planted_broken_link_returns_404(shop_urls: dict[str, str]) -> None:
    with pytest.raises(HTTPError) as error:
        urlopen(shop_urls["a11y-seo"] + "/livraison.html")
    assert error.value.code == 404
