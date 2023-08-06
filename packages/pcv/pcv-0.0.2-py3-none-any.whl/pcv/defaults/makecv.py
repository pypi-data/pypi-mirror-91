# -*- coding: utf-8 -*-
import shutil
from pcv import render, DIST_PATH, STATIC_PATH, STATIC
import settings  # noqa (module will be created by start.py)


# copy static content
if STATIC_PATH.exists():
    # copy static content to distribution folder
    shutil.copytree(STATIC_PATH, DIST_PATH.joinpath(STATIC), dirs_exist_ok=True)

# render templates to output file
with DIST_PATH.joinpath(settings.FILENAME).open('w', encoding='utf-8') as o:
    o.write(render(settings=settings))
