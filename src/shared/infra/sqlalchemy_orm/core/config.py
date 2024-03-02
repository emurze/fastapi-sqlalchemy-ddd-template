import os
from pathlib import Path

WORKDIR = os.getenv("WORKDIR", "")

PATH = Path(f"{WORKDIR}src/")

FILENAME = "tables.py"

CONTRACT_VARNAME = "contract"
