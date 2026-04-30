import sys
sys.path.insert(0, 'src')

from app import app

print("Checking bike-related routes in Flask app:")
for rule in app.url_map.iter_rules():
    if 'bike' in str(rule) or 'clear' in str(rule):
        print(f"  {rule.rule} -> {rule.endpoint}")

print("\nAll POST routes:")
for rule in app.url_map.iter_rules():
    if 'POST' in str(rule.methods):
        print(f"  {rule.rule} -> {rule.endpoint}")
