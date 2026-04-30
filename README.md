# Incident Tracker

## Overview
The Incident Tracker is a desktop application designed to help manage and track incidents related to personal protective equipment (PPE) compliance among drivers at a work station. The application allows users to upload a list of drivers, record incidents for missing equipment, and monitor the number of non-compliance records against each driver.

## Features
- Upload an Excel file containing a list of drivers with their Transporter IDs and names.
- Record incidents by entering the Transporter ID or Driver Name.
- Check boxes for missing equipment: High Visibility Vest and Safety Shoes.
- Automatically track non-compliance records against drivers.
- Notify users when a driver reaches 3 non-compliance records, indicating that escalation to DSP is required.

## Project Structure
```
incident-tracker
├── src
│   ├── app.py                  # Main entry point of the application
│   ├── components
│   │   └── incident_form.py    # User interface for recording incidents
│   ├── models
│   │   └── driver.py           # Driver model definition
│   ├── services
│   │   ├── excel_importer.py   # Functions for importing driver data from Excel
│   │   └── non_compliance_manager.py    # Logic for managing non-compliance records against drivers
│   └── storage
│       ├── database.py         # Database connection and operations
│       └── schema.sql          # SQL schema for database setup
├── data
│   └── .gitkeep                # Keeps the data directory tracked by version control
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using:
   ```
   pip install -r requirements.txt
   ```
4. Run the application using:
   ```
   python src/app.py
   ```

## Usage Guidelines
- To upload the current DA list, use the upload feature in the application.
- Enter the Transporter ID or Driver Name to record an incident.
- Select the appropriate checkboxes for the missing PPE.
- Input the incident date and submit the form.
- Monitor non-compliance records for each driver and receive notifications for escalation when necessary.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.