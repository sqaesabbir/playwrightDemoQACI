import re
import pytest
from playwright.sync_api import sync_playwright, expect


@pytest.fixture(scope="session")
def browser():
    # Initialize the browser session
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
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
    yield page
    page.close()


def test_text_box_interaction(page):
    # Perform actions related to the Text Box test without reloading the base URL
    page.locator("text=Elements").click()  # Use `locator` for text-based navigation
    page.locator("text=Text Box").click()

    # Fill in the text box form
    page.locator("[name='userName']").fill("Md.SABBIR HOSSAIN")
    page.locator("#userEmail").fill("sabbir@gmail.com")
    page.locator("#currentAddress").fill("123 Main St, Apt 4B, New York, NY 10001")
    page.locator("#permanentAddress").fill("123 Main St, Apt 4B, New York, NY 10001")
    page.locator("button:has-text('Submit')").click()  # Adjusted button locator

    # Wait for confirmation message or specific element after submission
    page.locator('text="Form submitted successfully"').wait_for(timeout=5000)
    expect(page.locator('text="Form submitted successfully"')).to_be_visible()


def test_check_box_and_radio_button(page):
    # Continue from the existing page state for Check Box and Radio Button test
    page.locator("text=Check Box").click()
    page.locator("label:has-text('Home')").click()  # Click on a checkbox

    # Ensure the file link is visible
    file_link = page.locator('text="Excel File.doc"')
    expect(file_link).to_be_visible()

    # Interact with the Radio Button
    page.locator("text=Radio Button").click()
    page.locator('text="Impressive"').wait_for(timeout=5000)
    expect(page.locator('text="Impressive"')).to_be_visible()
