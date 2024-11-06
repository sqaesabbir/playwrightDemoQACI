import re
import time

import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture(scope="session")
def browser():
    # Initialize the browser session
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True)
        context.tracing.stop(path="trace.zip")
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def page(browser):
    # Open the base page only once in the session scope
    DEMOQA_URL = "https://demoqa.com/"
    page = browser.new_page()
    page.goto(DEMOQA_URL)
    time.sleep(2)
    yield page
    page.close()


def test_text_box_interaction(page):
    # Perform actions related to the Text Box test without reloading the base URL
    page.locator("text=Elements").click()  # Use `locator` for text-based navigation
    page.locator("text=Text Box").click()

    # Fill in the text box form
    page.get_by_role("textbox", name="Full Name").fill("Md.SABBIR HOSSAIN")
    page.locator("#userEmail").fill("sabbir@gmail.com")
    page.locator("#currentAddress").fill("123 Main St, Apt 4B, New York, NY 10001")
    page.locator("#permanentAddress").fill("123 Main St, Apt 4B, New York, NY 10001")
    page.get_by_role("button").click()




def test_check_box_and_radio_button(page):

    page.get_by_text("Check Box").click()
    page.get_by_label("Toggle").click()
    page.locator("li").filter(has_text=re.compile(r"^Downloads$")).get_by_label("Toggle").click()

    # Ensure the file link is visible
    file_link = page.locator('text="Excel File.doc"')
    expect(file_link).to_be_visible()
    # Interact with the Radio Button
    page.locator("text=Radio Button").click()
    page.locator('text="Impressive"').wait_for(timeout=5000)
    expect(page.locator('text="Impressive"')).to_be_visible()
