from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.remote.webdriver import WebDriver

from selenium.common.exceptions import TimeoutException
from .Milestone import Milestone
from selenium.webdriver.common.action_chains import ActionChains
from .Website import retry_until_success
import logging
import time
import random
from ..Log.logging_config import setup_logger
setup_logger()



TIMEOUT = 30

class Container:
    '''
    The Container class represents a single container of a shipment. 
    Each container has a container ID, a expand button, a milestone panel, and a list of milestones.
    The container class is initialized by providing a container element and a WebDriver instance of the full page.
    The container class is responsible for extracting the container ID, expand button, milestone panel, and milestones.
    The container class is also responsible for clicking the expand button, and getting the milestone panel and milestones.
    Each container can, and oftentimes, have multiple milestones.
    '''
    def __init__(self, container_element: WebElement, page: WebDriver):
        self.container_page = page # the page where the container is located
        self.container_element = container_element # the actual container element
    
        self.container_id: str = self.get_container_id() # extract container ID
        self.expand_button: WebElement | None = self.get_expand_button() # check if there is expand button
        # if there is no expand button, it is high likely the container is the first one out of nth containers in a shipment.
        # in this case, the milestone panel is already expanded
        # if there is an expand button, check if not clicked yet, if not, it must be clicked so that milestone panel become visible, disregard if already expanded

        # get the milestone panel ID
        # the milestone panel ID is referenced by expand button attribute, because expand button is the one who make it visible
        # however, in case of there is no existing expand button, it will be default ID, this only happens to the first containers of every shipments.
        self.milestones_panel_id: str = self.get_milestones_panel_id(self.expand_button)

        # click expand so milestone panel become visible, if already expanded or expand button does not exist, it will be disregarded
        self.milestones_panel: WebElement | None = None  
        self.click_expand_button()  # this must initialize milestones panel as well if button isn't clicked yet
        # In case of the button is not existing or already clicked, get the milestones panel
        self.milestones_panel = self.get_milestones_panel(self.milestones_panel_id) if self.milestones_panel is None else self.milestones_panel
       
        self.milestones: list[Milestone] = self.get_milestones(self.milestones_panel)
        assert len(self.milestones) > 0
        self.is_complete: bool = "empty container return" in self.milestones[-1].event.lower()
        time.sleep(random.randint(2, 5))


    def get_container_id(self) -> str:
        def func():
            logging.info("Getting container ID...")
            container_id_element = WebDriverWait(self.container_element, TIMEOUT).until(
                    EC.visibility_of_element_located((By.TAG_NAME, "span"))
                )
            
            logging.info(f"Extracted Container ID: {container_id_element.text.strip()}")
                
            return container_id_element.text.strip()

        return retry_until_success(
            func=func,
            max_retries=3,
            delay=2,
            exceptions=(TimeoutError, TimeoutException),
            on_fail_message="Failed to get container ID. Retrying...",
            on_fail_execute_message="Failed to get container ID after 3 attempts"
        )
    

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
            # Expand button may not be present in the first container, because it is already expanded in default.
            logging.info(f"Expand button not found in container {self.container_id}.")
            return None
        
    def click_expand_button(self):
        def func():
            if not self.expand_button:
                logging.info(f"Expand button does not exist in container {self.container_id}, expanding button skipped.")
                return
            if self.expand_button.get_attribute("aria-expanded") == "false":
                
                actions = ActionChains(self.container_page)
                actions.move_to_element(self.expand_button).click().perform()

                logging.info(f"Expand button clicked in container {self.container_id}.")
                try:
                    self.milestones_panel = self.get_milestones_panel(self.milestones_panel_id)
                except Exception:
                    raise TimeoutException
                
               
        retry_until_success(
            func=func,
            max_retries=3,
            delay=2,
            exceptions=(TimeoutException),
            on_fail_message="Failed to click expand button. Retrying...",
            on_fail_execute_message="Failed to click expand button after 3 attempts"
        )
        
        logging.info(f"Expand button already expanded in container {self.container_id}.")
        
    def get_milestones_panel(self, milestones_panel_id):
        def func():
            milestones_panel = WebDriverWait(self.container_element, TIMEOUT).until(
                        EC.visibility_of_element_located(
                            (By.ID, milestones_panel_id)
                        )
                    )
            logging.info(f"Found milestones panel in container {self.container_id}.")
            return milestones_panel
        return retry_until_success(
            func=func,
            max_retries=10,
            delay=2,
            exceptions=(TimeoutError, TimeoutException),
            on_fail_message="Failed to get milestones panel. Retrying...",
            on_fail_execute_message="Failed to get milestones panel after 3 attempts"
        )

        
    def get_milestones(self, milestones_panel):
        def func():
            milestones = WebDriverWait(milestones_panel, TIMEOUT).until(
                EC.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "milestone")
                )
            )
            logging.info(f"Found {len(milestones)} milestones in container {self.container_id}.")
            return [Milestone(milestone_element) for milestone_element in milestones]
        
        return retry_until_success(
            func=func,
            max_retries=3,
            delay=2,
            exceptions=(TimeoutError, TimeoutException),
            on_fail_message="Failed to get milestones. Retrying...",
            on_fail_execute_message="Failed to get milestones after 3 attempts"
        )


    def get_milestones_panel_id(self, expand_button):
        if not expand_button:
            return "transport-plan__container__0"
        panel_id = expand_button.get_attribute("aria-controls")
        return panel_id
    
   

    

    

    
