import sys
import shutil
from pathlib import Path
import logging
from pcv import DEFAULTS_PATH, CALLER_PATH, SOURCE, STATIC, DIST

""" 
Initializes a pcv project in the current folder.

Run from command line: 
    
    python -m pcv.start
     
This will create the following directory tree in the current folder:

    .
    ├── settings.py
    ├── makecv.py
    ├── dist (empty directory)
    └── source
        ├── static (empty directory)
        └── template.json

"""

logger = logging.getLogger(__name__)


def initialize(destination=None):
    """ copy defaults tree to specified destination and create empty folders """
    if destination is None:
        destination = CALLER_PATH
    else:
        destination = Path(destination)
    path = shutil.copytree(DEFAULTS_PATH, destination, dirs_exist_ok=True)
    destination.joinpath(SOURCE).joinpath(STATIC).mkdir(exist_ok=True)
    destination.joinpath(DIST).mkdir(exist_ok=True)
    logger.info(f'pcv project initialized in {path}')


if __name__ == '__main__':
    logger.info(f'script path: {sys.argv.pop(0)}')
    initialize(*sys.argv)
