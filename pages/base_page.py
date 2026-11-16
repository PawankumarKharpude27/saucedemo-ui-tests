from __future__ import annotations

import re
from decimal import Decimal

from playwright.sync_api import Locator, Page, expect

_MONEY_RE = re.compile(r"\$(\d+(?:\.\d{2})?)")


def parse_money(text: str) -> Decimal:
    """'Item total: $39.98' -> Decimal('39.98'). Decimal avoids float rounding noise."""
    match = _MONEY_RE.search(text)
    if not match:
        raise ValueError(f"No money amount found in {text!r}")
    return Decimal(match.group(1))


class BasePage:
    """Shared plumbing. Pages expose locators and intent-level actions; assertions
    about *business outcomes* stay in the tests, assertions about *page readiness*
    live here (expect_loaded)."""

    path = "/"
    title_text: str | None = None

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self):
        self.page.goto(self.path)
        self.expect_loaded()
        return self

    def tid(self, test_id: str) -> Locator:
        return self.page.get_by_test_id(test_id)

    @property
    def title(self) -> Locator:
        return self.tid("title")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(re.compile(re.escape(self.path) + r"$"))
        if self.title_text:
            expect(self.title).to_have_text(self.title_text)

    def money(self, locator: Locator) -> Decimal:
        """Read a price: wait for a $ amount to render (web-first), then parse it."""
        expect(locator).to_contain_text("$")
        return parse_money(locator.inner_text())

    def money_list(self, locator: Locator) -> list[Decimal]:
        locator.first.wait_for()
        return [parse_money(t) for t in locator.all_inner_texts()]
