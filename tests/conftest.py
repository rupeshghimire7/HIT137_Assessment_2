"""Pytest configuration for test discovery and import paths."""

import sys
from pathlib import Path

# Add project root to path so imports work
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))