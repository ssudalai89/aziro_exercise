import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Configure logging (can be moved to framework-level config)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class HomePage:
    def __init__(self,driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    home_page_table_locator = (By.CSS_SELECTOR, "table.table.table-sm.table-hover.table-responsive-sm.small")
    expected_columns = ["","Website", "","Sales Revenue", "Tech Spend", "Products", "Followers", "Employees", "Traffic Rank",""]
    headers_locator = (By.TAG_NAME, "th")
    rows_locator = (By.TAG_NAME, "tr")
    cells_locator = (By.TAG_NAME, "td")
    dropdown_arrow_locator = (By.CSS_SELECTOR, "td.text-right.chev .icon-chevron-down")

    def load(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.home_page_table_locator)))
        logging.info("Home page loaded successfully")
        
    def title_validation(self,expected_title):
        try:
            self.wait.until(EC.title_is(expected_title))
            actual_title = self.driver.title
            logging.info(f"Actual title: {actual_title}, Expected title: {expected_title}")
            assert actual_title == expected_title, f"Title mismatch: Expected '{expected_title}', but got '{actual_title}'"
            logging.info("Title validation passed.")
        except TimeoutException:
            logging.error(f"Title did not match expected '{expected_title}' within the timeout period.")
            raise
        except AssertionError as e:
            logging.error(str(e))
            raise

    def get_table_columns(self):
        try:
            table = self.wait.until(EC.presence_of_element_located(self.home_page_table_locator))
            headers = table.find_elements(*self.headers_locator)
            column_names = [header.text.strip() for header in headers]
            logging.info(f"Table columns found: {column_names}")
            if column_names != self.expected_columns:
                logging.error(f"Expected columns {self.expected_columns}, but got {column_names}")
                raise AssertionError(f"Expected columns {self.expected_columns}, but got {column_names}")
            return column_names
        except TimeoutException:
            logging.error("Table not found within the timeout period.")
            raise
        except NoSuchElementException:
            logging.error("Table headers not found.")
            raise

    def check_column_headers_not_empty(self):
        try:
            table = self.wait.until(EC.presence_of_element_located(self.home_page_table_locator))
            headers = table.find_elements(*self.headers_locator)
            column_names = [header.text.strip() for header in headers]
            for col in column_names:
                if not col:
                    logging.error(f"Column header value is empty: {col}")
                    raise AssertionError(f"Column header value is empty: {col}")
            logging.info("All column header values are non-empty.")
            return column_names
        except TimeoutException:
            logging.error("Table not found within the timeout period.")
            raise
        except NoSuchElementException:
            logging.error("Table headers not found.")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in check_column_headers_not_empty: {str(e)}")
            raise

    def get_traffic_rank_for_website(self, website_name):
        try:
            parts = website_name.split(".")
            domain = ".".join(parts[-2:])
            # Find row based on main domain
            row_xpath = f"//tr[@data-domain='{domain}']"
            row = self.wait.until(
                EC.presence_of_element_located((By.XPATH, row_xpath))
            )
            cells = row.find_elements(By.TAG_NAME, "td")
            # Traffic Rank is always at index 8
            traffic_rank = cells[8].text.strip().replace(",", "")
            logging.info(f"Traffic rank for {website_name} is {traffic_rank}")
            return traffic_rank
        except TimeoutException:
            logging.error("Table or row not found within the timeout period.")
            raise
        except NoSuchElementException:
            logging.error("Table row or cells not found.")
            raise
        except IndexError:
            logging.error("Traffic rank cell index out of range.")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in get_traffic_rank_for_website: {str(e)}")
            raise

    def verify_dropdowns_have_data(self):
        try:
            # Scroll to bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logging.info("Scrolled to bottom of the page.")

            # Find all dropdown arrow buttons
            dropdown_arrows = self.driver.find_elements(*self.dropdown_arrow_locator)
            assert dropdown_arrows, "No dropdown arrows found on the page."
            logging.info(f"Found {len(dropdown_arrows)} dropdown arrows.")

            non_empty_count = 0
            for idx, arrow in enumerate(dropdown_arrows):
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", arrow)
                    arrow.click()
                    logging.info(f"Clicked dropdown arrow {idx+1}.")
                    parent_row = arrow.find_element(By.XPATH, "ancestor::tr")
                    next_row = parent_row.find_element(By.XPATH, "following-sibling::tr[1]")
                    cells = next_row.find_elements(By.TAG_NAME, "td")
                    cell_texts = [cell.text.strip() for cell in cells]
                    logging.info(f"Dropdown {idx+1} revealed row data: {cell_texts}")
                    if any(cell_texts):
                        non_empty_count += 1
                    else:
                        logging.warning(f"Dropdown {idx+1} revealed row is empty. Skipping.")
                except Exception as e:
                    logging.error(f"Error verifying dropdown {idx+1}: {str(e)}")
            if non_empty_count == 0:
                raise AssertionError("All dropdowns revealed empty rows.")
            logging.info(f"{non_empty_count} dropdowns revealed non-empty data.")
        except Exception as e:
            logging.error(f"Error in verify_dropdowns_have_data: {str(e)}")
            raise

    def verify_company_details_in_dropdown(self, expected_fields=None):
            """
            After expanding each dropdown, check for presence and correctness of company details.
            expected_fields: list of expected field names (e.g., ["Company Name", "Location", "Telephones", "Contacts"])
            """
            if expected_fields is None:
                expected_fields = ["Company Name", "Location", "Telephones", "Contacts"]
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                logging.info("Scrolled to bottom of the page.")

                dropdown_arrows = self.driver.find_elements(*self.dropdown_arrow_locator)
                assert dropdown_arrows, "No dropdown arrows found on the page."
                logging.info(f"Found {len(dropdown_arrows)} dropdown arrows.")

                for idx, arrow in enumerate(dropdown_arrows):
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", arrow)
                        arrow.click()
                        logging.info(f"Clicked dropdown arrow {idx+1}.")
                        parent_row = arrow.find_element(By.XPATH, "ancestor::tr")
                        next_row = parent_row.find_element(By.XPATH, "following-sibling::tr[1]")
                        # Assume expanded details are in a single td with inner HTML
                        detail_cells = next_row.find_elements(By.TAG_NAME, "td")
                        assert detail_cells, f"No detail cells found for dropdown {idx+1}."
                        detail_html = detail_cells[0].get_attribute("innerHTML")
                        logging.info(f"Dropdown {idx+1} detail HTML: {detail_html}")

                        # Parse the HTML as lines, stripping tags and splitting by line breaks
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(detail_html, "html.parser")
                        lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
                        logging.info(f"Dropdown {idx+1} parsed lines: {lines}")

                        for field in expected_fields:
                            try:
                                idx_field = next(i for i, l in enumerate(lines) if field.lower() in l.lower())
                                # Value is next non-empty line after field
                                value = None
                                for next_line in lines[idx_field+1:]:
                                    if next_line and next_line.lower() not in [f.lower() for f in expected_fields]:
                                        value = next_line
                                        break
                                assert value, f"Value for '{field}' is empty or not found in dropdown {idx+1}."
                                logging.info(f"Field '{field}' found with value '{value}' in dropdown {idx+1}.")
                            except StopIteration:
                                logging.error(f"Field '{field}' not found in dropdown {idx+1} details.")
                                raise AssertionError(f"Field '{field}' not found in dropdown {idx+1} details.")
                    except Exception as e:
                        logging.error(f"Error verifying company details in dropdown {idx+1}: {str(e)}")
                        raise
                logging.info("All dropdowns verified for company details.")
            except Exception as e:
                logging.error(f"Error in verify_company_details_in_dropdown: {str(e)}")
                raise