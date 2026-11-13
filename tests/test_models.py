from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from shop_auditor.models import AuditReport


def report_data(**overrides: Any) -> dict[str, Any]:
    finding = {
        "id": "f1",
        "axis": "ecommerce",
        "title": "Bouton panier invisible sur mobile",
        "severity": "critical",
        "evidence_ref": "pages/product/mobile/ecommerce/cta_above_fold",
        "evidence_summary": "Bouton à 1 240 px du haut, écran de 667 px",
        "recommendation": "Remonter le bouton sous le prix",
        "effort": "low",
        "impact": "high",
        "pages": ["product"],
    }
    data: dict[str, Any] = {
        "site_url": "https://exemple.fr",
        "platform": "shopify",
        "audited_at": datetime(2026, 11, 13, tzinfo=UTC),
        "pages": [{"id": "product", "url": "https://exemple.fr/p", "page_type": "product"}],
        "scores": {"performance": 72, "ecommerce": 40},
        "summary": "Une ligne.",
        "findings": [finding],
        "quick_wins": ["f1"],
        "limitations": [],
    }
    return data | overrides


def test_valid_report_round_trips_through_json() -> None:
    report = AuditReport.model_validate(report_data())
    assert AuditReport.model_validate_json(report.model_dump_json()) == report


@pytest.mark.parametrize(
    "overrides",
    [
        {"quick_wins": ["unknown"]},
        {"quick_wins": ["f1"] * 6},
        {"scores": {"performance": 101}},
        {"scores": {"not_an_axis": 50}},
        {"summary": "1\n2\n3\n4\n5\n6"},
        {"findings": [report_data()["findings"][0]] * 2},
        {"pages": []},  # finding references page "product" which no longer exists
        {"extra_field": "invented by the LLM"},
    ],
)
def test_invalid_report_is_rejected(overrides: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        AuditReport.model_validate(report_data(**overrides))
