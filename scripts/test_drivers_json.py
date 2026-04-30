from pathlib import Path
import sys
sys.path.insert(0, str(Path('src').resolve()))

from app import app, init_db

with app.app_context():
    init_db(app)
    rv = app.view_functions['drivers_json']()
    try:
        print(rv.get_data(as_text=True))
    except Exception:
        print(rv)
