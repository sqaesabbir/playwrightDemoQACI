import re
import time

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
    demo_url = "https://demoqa.com/"
    page = browser.new_page()
    page.goto(demo_url)
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


def test_check_box_and(page):
    page.get_by_text("Check Box").click()
    page.get_by_label("Toggle").click()
    page.locator("li").filter(has_text=re.compile(r"^Downloads$")).get_by_label("Toggle").click()

    # Ensure the file link is visible
    file_link = page.locator('text="Excel File.doc"')
    expect(file_link).to_be_visible()


def test_radio_button(page):
    # Interact with the Radio Button
    page.locator("text=Radio Button").click()
    page.get_by_text("Impressive").click()
    expect(page.get_by_text("You have selected Impressive")).to_be_visible()


def test_Web_Tables(page):
    page.get_by_text("Web Tables").click()
    expect(page.get_by_role("heading", name="Web Tables")).to_be_visible()
    add_data_to_the_table(page)
    verify_table_data(page, expected_data)


def add_data_to_the_table(page):
    page.locator("#addNewRecordButton").click()
    expect(page.locator('.modal-title')).to_be_visible()
    page.locator("#firstName").fill("Sabbir")
    page.locator("#lastName").fill("Hossain")
    page.locator("#userEmail").fill("cse.sabbirhossain@gmail.com")
    page.get_by_placeholder("Age").fill("24")

    page.get_by_placeholder("Salary").fill("5000")

    page.get_by_placeholder("Department").fill("SQA")
    page.locator("#submit").click()
    time.sleep(5)

def verify_table_data(page, expected_data):
    # Select all rows within the table body
    rows = page.query_selector_all('.rt-tbody .rt-tr')

    # Flag to check if match is found
    match_found = False

    # Helper function to normalize the data (strip unwanted characters)
    def normalize_text(text):
        return re.sub(r'[^\w\s]', '', text).strip()

    # Iterate over each row and check if it matches the expected data
    for i, row in enumerate(rows):
        cells = row.query_selector_all('.rt-td')

        # Extract and normalize text content of all cells in the row
        cell_texts = [normalize_text(cell.inner_text().strip()) for cell in cells]

        # Compare the normalized row's cell texts with the normalized expected data
        if cell_texts == expected_data:
            print(f"Match found in row {i + 1}!")
            match_found = True
            break  # Stop after finding the first match

    # If no match was found after checking all rows, raise an error
    if not match_found:
        raise AssertionError(f"Expected data {expected_data} not found in any row.")

# Sample expected data to verify
expected_data = [
    "Sabbir", "Hossain", "24", "cse.sabbirhossain@gmail.com", "5000", "SQA"
]