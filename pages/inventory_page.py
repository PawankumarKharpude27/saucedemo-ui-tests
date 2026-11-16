from __future__ import annotations

from decimal import Decimal
from enum import Enum

from playwright.sync_api import Locator

from .base_page import BasePage


class SortOption(str, Enum):
    NAME_AZ = "Name (A to Z)"
    NAME_ZA = "Name (Z to A)"
    PRICE_LOW_HIGH = "Price (low to high)"
    PRICE_HIGH_LOW = "Price (high to low)"


class InventoryPage(BasePage):
    path = "/inventory.html"
    title_text = "Products"

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
    def sort_dropdown(self) -> Locator:
        return self.tid("product-sort-container")

    @property
    def cart_badge(self) -> Locator:
        return self.tid("shopping-cart-badge")

    @property
    def cart_link(self) -> Locator:
        return self.tid("shopping-cart-link")

    # ---- per-product helpers (looked up by visible name, not by slug) ----
    def item(self, name: str) -> Locator:
        return self.items.filter(has=self.page.get_by_text(name, exact=True))

    def add_button(self, name: str) -> Locator:
        return self.item(name).get_by_role("button", name="Add to cart")

    def remove_button(self, name: str) -> Locator:
        return self.item(name).get_by_role("button", name="Remove")

    def add_to_cart(self, *names: str) -> None:
        for name in names:
            self.add_button(name).click()

    # ---- actions / reads ----
    def sort_by(self, option: SortOption) -> None:
        self.sort_dropdown.select_option(label=option.value)

    def read_names(self) -> list[str]:
        self.names.first.wait_for()
        return self.names.all_inner_texts()

    def read_prices(self) -> list[Decimal]:
        return self.money_list(self.prices)

    def open_cart(self) -> None:
        self.cart_link.click()
