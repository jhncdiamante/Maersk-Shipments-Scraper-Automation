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

    
if __name__ == "__main__":
    import pandas as pd
    # Example usage
    df = pd.read_excel(r"D:\vscode\ShipmentTracker\MSK Scrap DataFrame 2025-01-23--.xlsx")
        
    # Convert the first column to a list of BL numbers
    first_col_list = df.iloc[:, 0].dropna().unique().tolist()
    maersk = Maersk("https://www.maersk.com/tracking/")
    maersk.start(first_col_list[:5])
    data_list = []
    milestone_keys = {"Gate in", "Departure", "Arrival", "Discharge", "Gate out for delivery"}
    for shipment in maersk.shipments:
        
        for container in shipment.containers:

            milestones_data = {
                "Shipment ID": shipment.shipment_id,
                "Container ID": container.container_id,
                "Gate in": None,
                "Departure": None,
                "Arrival": None,
                "Discharge": None,
                "Gate out for delivery": None
            }
            for milestone in container.milestones:
                if milestone.event not in milestone_keys:
                    continue
                if (milestones_data[milestone.event] is not None and milestone.event not in ["Gate in", "Departure"]) or (milestones_data[milestone.event] is None):
                    milestones_data[milestone.event] = milestone.date
                    if milestone.event in ["Arrival", "Departure"]:
                        milestones_data[f"{milestone.event} Vessel Name"] = milestone.vessel_name
                        milestones_data[f"{milestone.event} Voyage ID"] = milestone.vessel_id 
            scrape_date = datetime.now().strftime("%m/%d/%y %H:%M %p")
            milestones_data['Scrape Date'] = scrape_date

            if not container.is_complete:
                for invalid_milestone in ['Arrival', 'Discharge', 'Gate out for delivery',
                                          'Arrival Vessel Name', 'Arrival Voyage ID']:
                    milestones_data[invalid_milestone] = None
                milestones_data['Estimated Arrival Time'] = container.milestones[-1].date
            else:
                milestones_data['Estimated Arrival Time'] = milestones_data['Arrival']
                    
            data_list.append(milestones_data)

    failed_df = pd.DataFrame(maersk.failed_shipment_ids, columns=["Failed Shipment IDs"])
    failed_df.to_csv("Failed_Shipment_Extractions.csv", index=False)
    df = pd.DataFrame(data_list)
    df.to_csv("OUTPUT.csv", index=False)
