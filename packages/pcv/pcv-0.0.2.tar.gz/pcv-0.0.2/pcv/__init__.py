# -*- coding: utf-8 -*-
import sys
import pathlib
import json
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pcv.filters import (
    reformat, as_circles, sort_and_group, sort_and_join_labels, kilo,
    sort_by_level_and_priority, group_by_category, minimum_level_and_priority)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# folder names
DEFAULTS = 'defaults'
SOURCE = 'source'
DIST = 'dist'
STATIC = 'static'
TEMPLATES = 'templates'
# package paths
PACKAGE_PATH = pathlib.Path(__file__).resolve().parent
DEFAULTS_PATH = PACKAGE_PATH.joinpath(DEFAULTS)
TEMPLATES_PATH = PACKAGE_PATH.joinpath(TEMPLATES)
# path to directory containing the script that invoked python interpreter
CALLER_PATH = pathlib.Path(sys.path[0]).resolve()
# project paths
SOURCE_PATH = CALLER_PATH.joinpath(SOURCE)
STATIC_PATH = SOURCE_PATH.joinpath(STATIC)
DIST_PATH = CALLER_PATH.joinpath(DIST)


def render(settings):
    # combine data from json files in a single dictionary
    data = dict()
    for filename in settings.JSON_FILES:
        with SOURCE_PATH.joinpath(filename).open('r') as file_obj:
            data.update(json.load(file_obj))
    # select items based on section settings
    for section_name, section_settings in settings.SECTIONS.items():
        # deal with sections based on other sections
        source_section_name = section_name
        if section_name not in data:
            source_section_name = section_settings['source']
            data[section_name] = dict(label=section_name)
        # exclude items based on level, priority, and exclusion list
        data[section_name]['list'] = minimum_level_and_priority(
            item_list=data[source_section_name]['list'],
            level=section_settings.get('level', 0),
            priority=section_settings.get('priority', float('inf')),
            exclude=section_settings.get('exclude', []))
    # configure template environment
    templates_paths = [SOURCE_PATH.joinpath(folder)
                       for folder in settings.TEMPLATE_FOLDERS]
    templates_paths.append(TEMPLATES_PATH)
    env = Environment(loader=FileSystemLoader(searchpath=templates_paths),
                      autoescape=select_autoescape(['html', 'css']))
    # register template filters
    env.filters['reformat'] = reformat
    env.filters['as_circles'] = as_circles
    env.filters['sort_and_group'] = sort_and_group
    env.filters['sort_and_join_labels'] = sort_and_join_labels
    env.filters['sort_by_level_and_priority'] = sort_by_level_and_priority
    env.filters['group_by_category'] = group_by_category
    env.filters['minimum_level_and_priority'] = minimum_level_and_priority
    env.filters['kilo'] = kilo
    # render pages
    return env.get_template('pages.html').render(settings=settings, **data)
