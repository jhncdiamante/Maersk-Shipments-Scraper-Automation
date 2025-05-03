from typing import Optional, Tuple
from selenium.webdriver.common.by import By
import re


class Milestone:
    def __init__(self, milestone_element):
        self.milestone_element = milestone_element
        self.event = self.milestone_element.find_element(By.TAG_NAME, "span").text.strip()
        
        self.date = self.milestone_element.find_element(By.CSS_SELECTOR, "span[data-test='milestone-date']").text.strip()
        self.vessel_id, self.vessel_name = self.extract_vessel_info(self.milestone_element.text.strip())
        self.event = "Arrival" if "arrival" in self.event.lower() else self.event
        self.event = "Departure" if "departure" in self.event.lower() else self.event
        
    def extract_vessel_info(self, status: str) -> Tuple[Optional[str], Optional[str]]:
        match = re.search(r"\((.+?) / (\w+)\)", status)
        if match:
            vessel_name = match.group(1).strip()
            voyage_id = match.group(2).strip()
            return voyage_id, vessel_name
        return None, None