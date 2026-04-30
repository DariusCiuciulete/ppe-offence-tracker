from app import app

print("All routes:")
for rule in app.url_map.iter_rules():
    print(f"  {rule}")

print("\nBike-related routes:")
for rule in app.url_map.iter_rules():
    if 'bike' in str(rule).lower():
        print(f"  {rule}")
