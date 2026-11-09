import sys
from pathlib import Path

# Add project root to sys.path
engine_root = Path(__file__).resolve().parent.parent
if str(engine_root) not in sys.path:
    sys.path.insert(0, str(engine_root))

