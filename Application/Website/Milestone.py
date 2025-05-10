from typing import Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re


class Milestone:
    def __init__(self, milestone_element: WebElement):
        self.milestone_element = milestone_element
        self.event: str = self.milestone_element.find_element(By.TAG_NAME, "span").text.strip()
        self.date: str = self.milestone_element.find_element(By.CSS_SELECTOR, "span[data-test='milestone-date']").text.strip()
        self.vessel_id, self.vessel_name = self.extract_vessel_info(self.milestone_element.text.strip())
        self.event: str = self.normalize_event(self.event)
        
    def extract_vessel_info(self, status: str) -> Tuple[Optional[str], Optional[str]]:
        match = re.search(r"\((.+?) / (\w+)\)", status)
        if match:
            vessel_name = match.group(1).strip()
            voyage_id = match.group(2).strip()
            return voyage_id, vessel_name
        return None, None

    def normalize_event(self, event) -> str:
        '''
        Normalize the event to a more consistent format. There are multiple types of arrival and departure milestone
        in the milestones panel.
        '''
        event = event.lower()
        if "arrival" in event:
            return "Arrival"
        elif "departure" in event:
            return "Departure"
        return event