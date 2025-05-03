from .Website import Website, retry_until_success

from datetime import datetime   
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from .Shipment import Shipment
import logging
import time

from ..Log.logging_config import setup_logger
setup_logger()




class Maersk(Website):
    def __init__(self, base_url):
        super().__init__(base_url)
        self._driver.get(self._base_url)
        logging.info(f"Opening homepage: {self._base_url}")
        self.confirm_cookies()

        self.shipments = []
        self.failed_shipment_ids = []

    def start(self, shipment_ids: list[str]):
        for shipment_id in shipment_ids:
            try:
                self.open_page(f"{self._base_url}{shipment_id}")
                self.shipments.append(Shipment(shipment_id, self._driver))
            except Exception as e:
                self.failed_shipment_ids.append(shipment_id)
                logging.error(f"Failed to extract shipment {shipment_id}: {e}")
                continue
    

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
            self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        
        retry_until_success(
            try_confirm_cookies,
            max_retries=3,
            delay=2,
            exceptions=(TimeoutException),
            on_fail_message="Failed to confirm cookies. Retrying...",
            on_fail_execute_message="Failed to confirm cookies after 3 attempts"
        )

    