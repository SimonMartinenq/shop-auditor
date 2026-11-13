"""Contracts between the collection phase and the analysis phase.

The collector writes a SiteSnapshot to disk; the agent reads it and returns an AuditReport.
"""

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Axis(StrEnum):
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"
    SEO = "seo"
    ECOMMERCE = "ecommerce"
    THIRD_PARTIES = "third_parties"
    VISUAL_ECO = "visual_eco"


class Severity(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"


class Level(StrEnum):
    """Used for both effort and impact."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Platform(StrEnum):
    SHOPIFY = "shopify"
    WOOCOMMERCE = "woocommerce"
    OTHER = "other"


class Viewport(StrEnum):
    MOBILE = "mobile"
    DESKTOP = "desktop"


class PageType(StrEnum):
    HOME = "home"
    COLLECTION = "collection"
    PRODUCT = "product"
    CART = "cart"
    CONTENT = "content"


class _Model(BaseModel):
    # Reject unknown fields: an LLM inventing a field must fail validation, not be ignored.
    model_config = ConfigDict(extra="forbid")


class PageRef(_Model):
    id: str
    url: str
    page_type: PageType


class PageSnapshot(_Model):
    """Raw measurements for one page. Each collector adds its own section in step 2."""

    page: PageRef
    screenshots: dict[Viewport, str] = {}  # PNG paths, relative to the run directory


class SiteSnapshot(_Model):
    site_url: str
    platform: Platform
    collected_at: datetime
    pages: list[PageSnapshot]


Score = Annotated[int, Field(ge=0, le=100)]


class Finding(_Model):
    id: str
    axis: Axis
    title: str
    severity: Severity
    evidence_ref: str  # points to a measurement in the snapshot; resolved by agent/checks.py
    evidence_summary: str
    recommendation: str
    effort: Level
    impact: Level
    pages: list[str]  # PageRef ids
    platform_hint: str | None = None


class AuditReport(_Model):
    site_url: str
    platform: Platform
    audited_at: datetime
    pages: list[PageRef]
    scores: dict[Axis, Score]  # computed in code from measurements, never by the LLM
    summary: str
    findings: list[Finding]
    quick_wins: list[str] = Field(max_length=5)  # Finding ids
    limitations: list[str]

    @model_validator(mode="after")
    def _check_internal_consistency(self) -> Self:
        """Checks that only need the report itself. Checks against the snapshot live in
        agent/checks.py."""
        if len(self.summary.strip().splitlines()) > 5:
            raise ValueError("summary must be 5 lines max")
        ids = [f.id for f in self.findings]
        if len(ids) != len(set(ids)):
            raise ValueError("finding ids must be unique")
        if unknown := set(self.quick_wins) - set(ids):
            raise ValueError(f"quick_wins reference unknown findings: {sorted(unknown)}")
        page_ids = {p.id for p in self.pages}
        for finding in self.findings:
            if unknown := set(finding.pages) - page_ids:
                raise ValueError(
                    f"finding {finding.id} references unknown pages: {sorted(unknown)}"
                )
        return self
