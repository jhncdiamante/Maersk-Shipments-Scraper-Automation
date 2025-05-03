from selenium.webdriver.remote.webelement import WebElement


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from Application.Website.Container import Container
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from .Website import retry_until_success
import logging

from ..Log.logging_config import setup_logger
setup_logger()


TIMEOUT = 180

class Shipment:
    def __init__(self, shipment_id: str, page: WebDriver):
        self.page = page
        self.shipment_id = shipment_id
        self.containers = self.get_containers()

    def get_containers(self): 
        def func():
            logging.info("Getting containers...")
            frame = WebDriverWait(self.page, TIMEOUT).until(
                        EC.visibility_of_element_located(
                        (By.CLASS_NAME, "track-grid__content")
                    )
                )

            containers = WebDriverWait(frame, TIMEOUT).until(
                EC.visibility_of_all_elements_located((By.XPATH, "./div"))
            )[1:]
            logging.info(f"Found {len(containers)} containers.")
            return [Container(container, self.page) for container in containers]
        return retry_until_success(
            func,
            max_retries=3,
            delay=2,
            exceptions=(TimeoutError, TimeoutException),
            on_fail_message="Failed to get containers. Retrying...",
            on_fail_execute_message="Failed to get containers after 3 attempts"
        )

    