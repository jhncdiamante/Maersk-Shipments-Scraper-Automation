from .Website import Website, retry_until_success

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from .Shipment import Shipment
import logging
from .SearchBar import SearchBar
import time
import random
from ..Log.logging_config import setup_logger
setup_logger()


class Maersk(Website):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.open_page(self._base_url)
        self._driver.maximize_window()
        self.confirm_cookies()
        self.search_bar = SearchBar(self._driver)

        self.shipments = [] # list of Shipment objects
        self.failed_shipments = [] # list of shipment ids that failed to process

    def start(self, shipment_ids: list[str]):
        for shipment_id in shipment_ids:
            
            self.search_bar.clear()
            self.search_bar.type_keyword(shipment_id)
            self.search_bar.click_search_button()
            try:
                self.shipments.append(Shipment(str(shipment_id), self._driver))
            except Exception as e:
                logging.error(f"Failed to process shipment {shipment_id}. Error: {e}")
                self.failed_shipments.append(shipment_id)
            finally:
                logging.info(f"Shipment {shipment_id} processed.")
                time.sleep(random.randint(3, 10))
    

    def confirm_cookies(self):  
        def try_confirm_cookies():
            logging.info("Confirming cookies...")
            cookies_button = self._wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, "button[data-test='coi-allow-all-button']"
                ))
            )
            cookies_button.click()
            logging.info("Cookies confirmed.")
          
        
        retry_until_success(
            try_confirm_cookies,
            max_retries=3,
            delay=2,
            exceptions=(TimeoutException),
            on_fail_message="Failed to confirm cookies. Retrying...",
            on_fail_execute_message="Failed to confirm cookies after 3 attempts"
        )

    def close(self):
        self._driver.close()

    