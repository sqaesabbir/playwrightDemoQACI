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



def add_data_to_the_table(page):
    page.locator("#addNewRecordButton").click()
    expect(page.locator('.modal-title')).to_be_visible()
    page.locator("#firstName").fill("Sabbir")
    page.locator("#lastName").fill("Hossain")
    email= page.locator("#userEmail").fill("cse.sabbirhossain@gmail.com")
    page.get_by_placeholder("Age").fill("24")
    page.get_by_placeholder("Salary").fill("5000")
    page.get_by_placeholder("Department").fill("SQA")
    page.locator("#submit").click()

    table_rows = page.get_by_role("row")

    # Get the count of rows
    row_count = table_rows.count()

    # Print the count or use it in an assertion
    print(f"Number of rows in the table: {row_count}")

    # Verify the row count (example assertion)
    expect(table_rows).to_have_count(11)
    time.sleep(2)

    email_cell = page.locator(f'.rt-td:has-text("cse.sabbirhossain@gmail.com")')

    # Ensure that the email is present in the table
    expect(email_cell).to_be_visible()
    time.sleep(2)




