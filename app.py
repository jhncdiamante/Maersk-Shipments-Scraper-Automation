from Application.Website.Maersk import Maersk
from datetime import datetime
import pandas as pd

INPUT_FILE_PATH = r"D:\vscode\ShipmentTracker\MSK Scrap DataFrame 2025-01-23--.xlsx"
if INPUT_FILE_PATH.endswith(".csv"):
    df = pd.read_csv(INPUT_FILE_PATH)
elif INPUT_FILE_PATH.endswith(".xlsx"):
    df = pd.read_excel(INPUT_FILE_PATH)
    
# Convert the first column to a list of BL numbers
first_col_list = df.iloc[:, 0].dropna().unique().tolist()
maersk = Maersk("https://www.maersk.com/tracking/")
maersk.start(first_col_list)
data_list = []

milestone_keys = {"Gate in", "Departure", "Arrival", "Discharge", "Gate out for delivery"}

try:

    # iterate through each shipment and its containers
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
                    continue  # skip unnecessary milestones

                # this control flow records the first occurrence of Gate in and Departure
                # and the last occurrence of Arrival, Discharge, and Gate out for delivery

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


except Exception as e:
    print(f"An error occurred: Stopping program. Error: {e}")
finally:
    failed_df = pd.DataFrame(maersk.failed_shipments, columns=["Failed Shipment IDs"])
    failed_df.to_csv("Failed_Shipment_Extractions.csv", index=False)

    df = pd.DataFrame(data_list)
    df.to_csv("OUTPUT.csv", index=False)

