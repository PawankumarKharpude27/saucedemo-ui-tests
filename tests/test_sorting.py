import pytest
from playwright.sync_api import expect

from pages import SortOption


@pytest.mark.regression
def test_sort_name_z_to_a(inventory_page):
    inventory_page.open()
    original = inventory_page.read_names()

    inventory_page.sort_by(SortOption.NAME_ZA)

    # Oracle = independently sorted copy of what the page showed before sorting.
    # to_have_text(list) retries until the DOM matches, so no sleeps are needed.
    expect(inventory_page.names).to_have_text(sorted(original, reverse=True))


@pytest.mark.regression
def test_sort_price_low_to_high(inventory_page):
    inventory_page.open()
    original = inventory_page.read_prices()

    inventory_page.sort_by(SortOption.PRICE_LOW_HIGH)

    expected = [f"${price:.2f}" for price in sorted(original)]
    expect(inventory_page.prices).to_have_text(expected)
