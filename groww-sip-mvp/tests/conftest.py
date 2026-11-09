import sys
from pathlib import Path

# Add MVP root to sys.path
mvp_root = Path(__file__).resolve().parent.parent
if str(mvp_root) not in sys.path:
    sys.path.insert(0, str(mvp_root))

