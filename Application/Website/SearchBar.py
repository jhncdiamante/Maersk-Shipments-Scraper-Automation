from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
from selenium.webdriver.common.keys import Keys

from ..Log.logging_config import setup_logger
setup_logger()

TIMEOUT = 180

class SearchBar:
    def __init__(self, driver):
        self.driver = driver
        # Find the mc-input element
        host = WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "mc-input#track-input")))

        # Access its shadow root
        shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", host)
        self.search_box = shadow_root.find_element(By.ID, "mc-input-track-input")
        logging.info("Search box found.")
        self.search_button = WebDriverWait(self.driver, TIMEOUT).until(EC.element_to_be_clickable((By.CLASS_NAME, "track__search__button")))
        logging.info("Search button found.")

    def clear(self):
        self.search_box.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        
        logging.info("Search box cleared.")

    def type_keyword(self, search_term):
        self.search_box.clear()
        logging.info(f"Typing keyword: {search_term}")
        self.search_box.send_keys(search_term)
        logging.info(f"Keyword typed: {search_term}")

    def click_search_button(self):
        action = ActionChains(self.driver)
        logging.info("Clicking search button...")
        action.move_to_element(self.search_button).click().perform()
        logging.info("Search button clicked.")
