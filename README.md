# Maersk Automated Shipment Data Collection (_Scraper_)
- A Selenium-based scraper system that automates data collection from the Maersk website.
- For educational, personal, and non-commercial use only.

## 📦 What Data Can Be Scraped Using a Single Shipment ID?

- **Shipment Status**
- **Containers**
  - Latest Event
  - Estimated Arrival Date
  - **Milestones**
    - Event Type
    - Date
    - Vessel Name & ID

        
## 📦 Features

✨ Automated Search — Searches for shipments based on tracking ID.

⚡ Data Retrieval — Retrieves shipment container details and their milestones.

🔒 Status Tracking — Tracks shipment status (e.g., ongoing, completed).

## 🛠️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/jhncdiamante/MaerskScraperAutomation.git
cd MaerskScraperAutomation
pip install -r requirements.txt
```
## Usage

### To start scraping:

```bash
from Application.Website.Maersk import Maersk

maersk = Maersk("https://www.maersk.com/tracking/")

maersk.start(["<placeholder>"]) # list of shipment IDs
# Access shipments
shipments = maersk.shipments # list of Shipment Objects
first_shipment = shipments[0]
print(f"Shipment ID: {first_shipment.shipment_id}")

# Access a single shipment containers
shipment_containers = first_shipment.containers # list of Container objects
number_of_extracted_containers = len(shipment_containers)
print(f"Number of containers: {number_of_extracted_containers}")

# Access each container

for idx, container in enumerate(shipment_containers):
    # Get container ID
    print(f"{idx + 1}. {container.container_id}")

    # Get status(bool): True = Complete
    status = "Completed" if container.is_complete else "On-going"
    print(f"Status: {status}")

    # Get container milestones from oldest to latest
    milestones = container.milestones

    print("\n>>>>> MILESTONES <<<<<\n")
    for idx, milestone in enumerate(milestones):
        # Get milestone event type e.g. Gate in
        event = milestone.event
        # Get event date
        date = milestone.date
        # OPTIONAL: Get milestone vessel name and ID
        # Available only in departure and arrival milestones
        vessel_name = milestone.vessel_name
        vessel_id = milestone.vessel_id
        milestone_data = f"{idx + 1}. {event}: {date}\n"
        if vessel_name and vessel_id:
            print(f"{milestone_data} Vessel: {vessel_name} ({vessel_id})\n")
        else:
            print(milestone_data)

maersk.close()
   

```
## Output

```bash

ShipmentID: 250653657
Number of containers: 1
1. MNBU0353275
Status: Completed

>>>>> MILESTONES <<<<<

1. Gate out Empty: 20 Mar 2025 20:34

2. Gate in: 24 Mar 2025 13:14

3. Load: 28 Mar 2025 04:35

4. Departure: 28 Mar 2025 19:13
Vessel: CELSIUS EINDHOVEN (012W)

5. Arrival: 03 Apr 2025 17:53
Vessel: CELSIUS EINDHOVEN (012W)

6. Discharge: 03 Apr 2025 20:43

7. Gate out: 03 Apr 2025 21:39

8. Gate in: 03 Apr 2025 22:07

9. Load: 07 Apr 2025 04:36

10. Departure: 07 Apr 2025 10:37
Vessel: MAERSK KENTUCKY (514W)

11. Arrival: 10 Apr 2025 20:44
Vessel: MAERSK KENTUCKY (514W)

12. Discharge: 10 Apr 2025 22:16

13. Load: 14 Apr 2025 05:58

14. Departure: 14 Apr 2025 13:47
Vessel: HOPE ISLAND (516N)

15. Arrival: 19 Apr 2025 06:05
Vessel: HOPE ISLAND (516N)

16. Discharge: 19 Apr 2025 15:31

17. Gate out for delivery: 20 Apr 2025 11:58

18. Empty container return: 21 Apr 2025 13:23
```

## Logging

The scraper includes logging for debugging purposes.  
It also serves as a useful guide for understanding how the tool operates, as it logs each step of the scraping process in detail.


## 🔮 Future Improvements

-  Inclusion of origin and destination countries/locations, milestone locations, last updated timestamp, and customizable actions.
-  Improve error handling and logging system
-  Cookie Caching for Pop-up Prevention
  

## ❗ Disclaimer ❗

This project is intended for **educational, personal, and non-commercial use only**.

It is **not affiliated with, endorsed by, or in any way officially connected to Maersk** or any of its subsidiaries or affiliates.

Users are solely responsible for how they use this tool.  

**Please ensure you comply with Maersk’s Terms of Service** and any applicable laws or regulations when accessing and using their website.

The creator of this project is **not liable** for any misuse or damage caused by using this scraper.









