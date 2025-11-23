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

# Configure logging (can be moved to framework-level config)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class BasePage:
    """Base Page class containing reusable Selenium operations"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- Waits ----------
    def wait_for_element_visible(self, locator):
        """Wait until element is visible"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            logging.info(f"Element visible: {locator}")
            return element
        except TimeoutException as e:
            logging.error(f"Timeout waiting for element visible: {locator}")
            raise e

    def wait_for_element_clickable(self, locator):
        """Wait until element is clickable"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            logging.info(f"Element clickable: {locator}")
            return element
        except TimeoutException as e:
            logging.error(f"Timeout waiting for element clickable: {locator}")
            raise e

    # ---------- Scroll ----------
    def scroll_to_element(self, locator):
        """Scroll to element using JavaScript"""
        try:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            logging.info(f"Scrolled to element: {locator}")
        except NoSuchElementException as e:
            logging.error(f"Element not found for scrolling: {locator}")
            raise e

    def scroll_page_down(self):
        """Scroll entire page down"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.info("Scrolled page down")

    def scroll_page_up(self):
        """Scroll entire page up"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        logging.info("Scrolled page up")

    # ---------- Click ----------
    def click(self, locator):
        """Scroll to and click an element"""
        try:
            self.scroll_to_element(locator)
            element = self.wait_for_element_clickable(locator)
            element.click()
            logging.info(f"Clicked element: {locator}")
        except (ElementClickInterceptedException, NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to click element: {locator} | {str(e)}")
            raise e

    # ---------- Type / Input ----------
    def enter_text(self, locator, text, clear_first=True):
        """Scroll to and enter text into input field"""
        try:
            self.scroll_to_element(locator)
            element = self.wait_for_element_visible(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            logging.info(f"Entered text into element: {locator} -> '{text}'")
        except NoSuchElementException as e:
            logging.error(f"Unable to locate element for entering text: {locator}")
            raise e

    # ---------- Getters ----------
    def get_text(self, locator):
        """Scroll to and get text of element"""
        try:
            self.scroll_to_element(locator)
            element = self.wait_for_element_visible(locator)
            text = element.text
            logging.info(f"Got text from element: {locator} -> '{text}'")
            return text
        except Exception as e:
            logging.error(f"Failed to get text from element: {locator} | {str(e)}")
            raise e

    def get_element_attribute(self, locator, attribute):
        """Scroll to and get element attribute"""
        try:
            self.scroll_to_element(locator)
            element = self.wait_for_element_visible(locator)
            value = element.get_attribute(attribute)
            logging.info(f"Got attribute '{attribute}' from {locator}: {value}")
            return value
        except Exception as e:
            logging.error(f"Failed to get attribute from element: {locator} | {str(e)}")
            raise e

    # ---------- Check ----------
    def is_element_displayed(self, locator):
        """Return True if element is displayed"""
        try:
            self.scroll_to_element(locator)
            element = self.driver.find_element(*locator)
            displayed = element.is_displayed()
            logging.info(f"Element displayed check: {locator} -> {displayed}")
            return displayed
        except NoSuchElementException:
            logging.error(f"Element not found for displayed check: {locator}")
            return False

    # ---------- ActionChains ----------
    def hover_over_element(self, locator):
        """Scroll to and hover over an element"""
        try:
            self.scroll_to_element(locator)
            element = self.wait_for_element_visible(locator)
            ActionChains(self.driver).move_to_element(element).perform()
            logging.info(f"Hovered over element: {locator}")
        except Exception as e:
            logging.error(f"Hover failed: {locator} | {str(e)}")
            raise e

    def press_key(self, key=Keys.ENTER):
        """Press a key on the active element"""
        try:
            ActionChains(self.driver).send_keys(key).perform()
            logging.info(f"Pressed key: {key}")
        except Exception as e:
            logging.error(f"Failed to press key: {key} | {str(e)}")
            raise e

    # ---------- Navigation ----------
    def open_url(self, url):
        """Open a given URL"""
        try:
            self.driver.get(url)
            logging.info(f"Opened URL: {url}")
        except Exception as e:
            logging.error(f"Failed to open URL: {url} | {str(e)}")
            raise e

    def get_page_title(self):
        """Return current page title"""
        title = self.driver.title
        logging.info(f"Page title: {title}")
        return title

    def get_current_url(self):
        """Return current URL"""
        url = self.driver.current_url
        logging.info(f"Current URL: {url}")
        return url
