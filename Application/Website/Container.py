from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.remote.webdriver import WebDriver

from selenium.common.exceptions import TimeoutException
from .Milestone import Milestone
from .Website import retry_until_success
import logging

from ..Log.logging_config import setup_logger
setup_logger()



TIMEOUT = 180

class Container:
    def __init__(self, container_element: WebElement, page: WebDriver):
        self.container_page = page
        self.container_element = container_element

        self.container_id: str = self.get_container_id()
        self.expand_button: WebElement | None = self.get_expand_button()
  
        self.miletones_pane_id: str = self.get_milestones_pane_id()
        self.click_expand_button()
        self.milestones: list[Milestone] = self.get_milestones()
        self.is_complete: bool = "Empty container return" in self.milestones[-1].event


    def get_container_id(self) -> str:
        logging.info("Getting container ID...")
        container_id_element = WebDriverWait(self.container_element, TIMEOUT).until(
                EC.visibility_of_element_located((By.TAG_NAME, "span"))
            )
        
        logging.info(f"Extracted Container ID: {container_id_element.text.strip()}")
            
        return container_id_element.text.strip()
    

    def get_expand_button(self):
        try:
            expand_button = WebDriverWait(self.container_element, TIMEOUT).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".container__toggle.toggle-button")
                )
            )
            logging.info(f"Expand button found in container {self.container_id}.")
            return expand_button
        except TimeoutException:
            logging.INFO(f"Expand button not found in container {self.container_id}.")
            return None
        
    def click_expand_button(self):
        if not self.expand_button:
            logging.info(f"Expand button does not exist in container {self.container_id}, expanding button skipped.")
            return
        if self.expand_button.get_attribute("aria-expanded") == "false":
            self.container_page.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", self.expand_button
            )
            self.expand_button.click()
            logging.info(f"Expand button clicked in container {self.container_id}.")
            WebDriverWait(self.container_element, TIMEOUT).until(
                EC.visibility_of_element_located(
                    (By.ID, self.miletones_pane_id)
                )
            )
        logging.info(f"Expand button already expanded in container {self.container_id}.")
        
    def get_milestones(self):
        try:
            milestones_pane = WebDriverWait(self.container_element, TIMEOUT).until(
                    EC.visibility_of_element_located(
                        (By.ID, self.miletones_pane_id)
                    )
                )
            milestones = WebDriverWait(milestones_pane, TIMEOUT).until(
                EC.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "milestone")
                )
            )
            logging.info(f"Found {len(milestones)} milestones in container {self.container_id}.")
            return [Milestone(milestone_element) for milestone_element in milestones]
        except TimeoutError: 
            return None

    def get_milestones_pane_id(self):
        if not self.expand_button:
            return "transport-plan__container__0"
        pane_id = self.expand_button.get_attribute("aria-controls")
        return pane_id
    
   

    

    

    
