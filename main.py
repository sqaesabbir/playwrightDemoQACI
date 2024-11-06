import re
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="session")
def browser():
    # Initialize the browser session
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
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
    page.get_by_text("Elements").click()
    page.get_by_text("Text Box").click()

    # Fill in the text box form
    page.get_by_role("textbox", name="Full Name").fill("Md.SABBIR HOSSAIN")
    page.locator("#userEmail").fill("sabbir@gmail.com")
    page.locator("#currentAddress").fill("123 Main St, Apt 4B, New York, NY 10001")
    page.locator("#permanentAddress").fill("123 Main St, Apt 4B, New York, NY 10001")
    page.get_by_role("button").click()

    # # Wait for confirmation message or specific element after submission
    # page.locator('text="Form submitted successfully"').wait_for(timeout=5000)

def test_check_box_and_radio_button(page):
    # Continue from the existing page state for Check Box and Radio Button test
    page.get_by_text("Check Box").click()
    page.get_by_label("Toggle").click()
    page.locator("li").filter(has_text=re.compile(r"^Downloads$")).get_by_label("Toggle").click()

    # Ensure the file link is visible
    file_link = page.locator('text="Excel File.doc"')
    expect(file_link).to_be_visible()

    # Interact with the Radio Button
    radio_button = page.get_by_text("Radio Button")
    radio_button.click()
    page.locator('text="Impressive"').wait_for(timeout=5000)
    expect(page.locator('text="Impressive"')).to_be_visible()
