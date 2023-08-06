import setuptools
from pathlib import Path

"""
create package:

    python setup.py sdist bdist_wheel
    
https://packaging.python.org/guides/distributing-packages-using-setuptools/

https://docs.python.org/3.8/distutils/setupscript.html#installing-package-data


we can also install the package locally using

	pipenv install -e .
    
"""


def glob_fix(package_name, glob):
    """
    todo: remove when setuptools supports the recursive glob pattern ('**')

    https://github.com/pypa/setuptools/issues/1806
    """
    # this assumes setup.py lives in the folder that contains the package
    package_path = Path(f'./{package_name}').resolve()
    # to include a directory recursively, use: '<dirname>/**/*'
    return [str(path.relative_to(package_path))
            for path in package_path.glob(glob)]


with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='pcv',
    version="0.0.2",
    author='D. van Gerwen',
    author_email='djvg@protonmail.com',
    description='Build a crisp CV (resume), as printable HTML, from JSON.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dennisvang/pcv/',
    packages=setuptools.find_packages(),
    package_data={'pcv': [*glob_fix('pcv', 'defaults/**/*'),
                          *glob_fix('pcv', 'templates/**/*')]},
    install_requires=['jinja2'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # for shutil.copytree dirs_exist_ok
)
