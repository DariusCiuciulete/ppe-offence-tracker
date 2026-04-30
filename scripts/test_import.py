import sys
from pathlib import Path
sys.path.insert(0, str(Path('src').resolve()))

try:
    import app
    print('app imported successfully')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
