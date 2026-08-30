import sys
from pathlib import Path


cipher_text = Path(__file__).parent.parent / "src" / "cipher_text"

sys.path.insert(0, str(cipher_text))