from __future__ import annotations

from decimal import Decimal

from playwright.sync_api import Locator

from .base_page import BasePage


class CheckoutInfoPage(BasePage):
    path = "/checkout-step-one.html"
    title_text = "Checkout: Your Information"

    @property
    def error(self) -> Locator:
        return self.tid("error")

    def fill_form(self, first_name: str = "", last_name: str = "", postal_code: str = "") -> None:
        self.tid("firstName").fill(first_name)
        self.tid("lastName").fill(last_name)
        self.tid("postalCode").fill(postal_code)

    def continue_(self) -> None:
        self.page.get_by_role("button", name="Continue").click()


class CheckoutOverviewPage(BasePage):
    path = "/checkout-step-two.html"
    title_text = "Checkout: Overview"

    @property
    def names(self) -> Locator:
        return self.tid("inventory-item-name")

    @property
    def prices(self) -> Locator:
        return self.tid("inventory-item-price")

    def item_prices(self) -> list[Decimal]:
        return self.money_list(self.prices)

    def subtotal(self) -> Decimal:
        return self.money(self.tid("subtotal-label"))

    def tax(self) -> Decimal:
        return self.money(self.tid("tax-label"))

    def total(self) -> Decimal:
        return self.money(self.tid("total-label"))

    def finish(self) -> None:
        self.page.get_by_role("button", name="Finish").click()


class CheckoutCompletePage(BasePage):
    path = "/checkout-complete.html"
    title_text = "Checkout: Complete!"

    @property
    def header(self) -> Locator:
        return self.tid("complete-header")
