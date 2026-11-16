from __future__ import annotations

from decimal import Decimal

from playwright.sync_api import Locator

from .base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"
    title_text = "Your Cart"

    @property
    def items(self) -> Locator:
        return self.tid("inventory-item")

    @property
    def names(self) -> Locator:
        return self.tid("inventory-item-name")

    @property
    def prices(self) -> Locator:
        return self.tid("inventory-item-price")

    @property
    def badge(self) -> Locator:
        return self.tid("shopping-cart-badge")

    def remove(self, name: str) -> None:
        self.items.filter(has=self.page.get_by_text(name, exact=True)).get_by_role(
            "button", name="Remove"
        ).click()

    def read_prices(self) -> list[Decimal]:
        return self.money_list(self.prices)

    def checkout(self) -> None:
        self.page.get_by_role("button", name="Checkout").click()

    def continue_shopping(self) -> None:
        self.page.get_by_role("button", name="Continue Shopping").click()
