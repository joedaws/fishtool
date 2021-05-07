import os
from pathlib import Path


home = str(Path.home())
LIBRARY_FILE = os.path.join(home, '.motherbrain/library.hdf5')

