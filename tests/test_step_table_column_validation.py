import pytest
import logging
from pages.home_page import HomePage
from selenium.webdriver.common.by import By


def test_home_page_table_column_validation(browser):
    """Test to validate the columns of the home page table."""
    try:
        home_page = HomePage(browser)
        home_page.load()
        home_page.title_validation("Websites using Responsive Tables")
        home_page.get_table_columns()
        logging.info("Table column validation test passed.")
    except Exception as e:
        logging.error(f"Table column validation test failed: {str(e)}")
        raise

def test_home_page_table_column_headers_not_empty(browser):
    """Test to validate that no column header value is empty."""
    try:
        home_page = HomePage(browser)
        home_page.load()
        home_page.get_table_columns()
        home_page.check_column_headers_not_empty()
        logging.info("No column header value is empty.")
    except Exception as e:
        logging.error(f"Column header empty value test failed: {str(e)}")
        raise
    
def test_traffic_rank_for_lists_rtcamp(browser):
    try:
        home_page = HomePage(browser)
        home_page.load()
        traffic_rank = home_page.get_traffic_rank_for_website("lists.rtcamp.com")
        assert traffic_rank == "373985", f"Expected 373,985 but got {traffic_rank}"
        logging.info(f"Verified traffic rank for lists.rtcamp.com: {traffic_rank}")
    except Exception as e:
        logging.error(f"Traffic rank test for lists.rtcamp.com failed: {str(e)}")
        raise

def test_dropdowns_reveal_data(browser):
    """Test to verify that each dropdown arrow reveals non-empty data."""
    try:
        home_page = HomePage(browser)
        home_page.load()
        # First, verify dropdowns reveal non-empty data
        home_page.verify_dropdowns_have_data()
        logging.info("All dropdowns reveal non-empty data.")

        # Then, verify company details in expanded dropdowns
        expected_fields = ["Company Name", "Location", "Telephones", "Contacts"]
        home_page.verify_company_details_in_dropdown(expected_fields=expected_fields)
        logging.info("All dropdowns contain expected company details.")
    except Exception as e:
        logging.error(f"Dropdown data and company details verification test failed: {str(e)}")
        raise