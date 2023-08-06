## About pcv

Pcv creates a printable curriculum vitae (resume) in HTML format, based on data stored in JSON.

The basic idea is to use JSON to store all data related to you resume, then use a settings file to tailor the displayed data to a specific job-application.

## History

The original intention was to create just any kind of mini-framework, from scratch (except for the template language), in order to gain some insight into framework architecture in general.
The specific choice to focus on resume creation was just convenient at the time.

## Status

The project is still in the early stages of development, so it is **not** production-ready.

There are many similar projects out there that are much more complete.

## Dependencies

Although we aim for a minimum number of external dependencies, we cannot do without `jinja2`.

YAML would be easier to write than JSON, but we don't want the extra dependency required (e.g. PyYAML).

Instead of using another external dependency to handle PDF creation (e.g. ReportLab or PyQT), we use CSS print styles so we can print to PDF using the browser. This is not the most convenient, but it works in most cases.

## Installation

Installation from pypi, using pipenv:

    pipenv install pcv

An alternative would be local installation using e.g. pipenv:

Either install into site packages using

	pipenv install <path to pcv-x.y.z.tar.gz>

or install as an [editable dependency](https://pipenv.pypa.io/en/latest/basics/#editable-dependencies-e-g-e), using 

	pipenv install -e <path to pcv/setup.py>

## Quick start

To start a new `pcv` project in the current folder, run the following from the command line:

    python -m pcv.start

This will create the following directory structure:

    .
    ├─ dist
    ├─ source
    │  ├─ static
    │  ├─ templates
    │  └─ cv_template.json
    ├─ settings.py
    └─ makecv.py

The quickest way to get started is to fill out the `cv_template.json` file with your details.

When `cv_template.json` is ready, call `makecv.py`:

    python makecv.py

This will create your resume, as an HTML file, in the `dist` folder.

Whenever you make a change to your JSON or settings, run `makecv.py` again.

## Settings

High level configuration of your resume can be accomplished using the `settings.py` file.

This file specifies the following constants:

#### FILENAME

Name of the output file that will be written to the `dist` folder.
Default: `'cv.html'` 

#### JSON_FILES

List of JSON source files. These are combined into a single python dictionary.
Default: `['cv_template.json']`

#### TEMPLATE_FOLDERS

List of names for folder that contain custom templates (relative to the project's `source` folder).
Default: `[]`

#### PAGES

List of page templates to include. 
Default page templates can be found in the pcv source: `pcv/templates/pages` 
Default: `['onepage.html', 'technologies.html', 'publications.html']`


#### STYLES

List of CSS stylesheets to include.
Default stylesheets can be found in the pcv source: `pcv/templates/styles`
Default: `['style_pages.css', 'style_zero.css']`

#### THEME_COLOR

Main theme color.
Default: `'#438496'`

#### THEME_FONT_COLOR

Main font color.
Default: `'white'`

#### SECTIONS

Dictionary with section-specific settings.
This dictionary specifies content filter levels, as follows:

    {
        <section name>: {
            'level': <minimum level>,
            'priority': <minimum priority>,
            'exclude': [<item to exclude>, ...],
            'source': <name of source section>
        }, 
        ...
    }

The section specification keys `level`, `priority`, `exclude`, and `source` are all optional.
Default section templates can be found in the pcv source: `pcv/templates/sections`
Default: 

    dict(technologies=dict(level=2, priority=2, exclude=[]), 
         skills=dict(level=3, priority=1, source='technologies'))
 
## Custom templates

### Overriding default templates

It is possible to override any of the `jinja2` templates in the source `pcv/templates` subdirectories.
To do so, copy the template to your project's `source/templates` folder, and place it in an appropriate subfolder, e.g. `pages` or `sections`.

For example, we can override the default `onepage.html` page by copying the file into our project's source folder: `source/templates/pages/onepage.html`

(TODO: actually this does not work yet)

### Custom pages

todo
