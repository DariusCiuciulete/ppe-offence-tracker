from storage.database import db, BikeIncident
from app import app

app.app_context().push()
incidents = BikeIncident.query.all()
print(f'Found {len(incidents)} bike incidents')
for i in incidents:
    print(f'  - {i.bike_type} {i.bike_serial}: missing_windscreen={i.missing_windscreen}, faulty_brake={i.faulty_brake}')
