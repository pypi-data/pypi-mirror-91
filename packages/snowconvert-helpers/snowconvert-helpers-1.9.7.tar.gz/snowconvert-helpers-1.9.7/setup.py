import setuptools
import codecs
import os
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


REQUIREMENTS = ['snowflake-connector-python>=2.3.6']

KEYWORDS = ['MOBILIZE',
            'SNOWFLAKE',
            'TERADATA',
            'BTEQ']

setuptools.setup(
    name="snowconvert-helpers",
    packages=['snowconverthelpers'],
    version=find_version('snowconverthelpers', '__init__.py'),
    license='SEE LICENSE IN LICENSE',
    description='Tool that emulates Teradata-BTEQ behavours and facilitates connections to Snowflake.',
    author='Mobilize.Net',
    author_email='info@mobilize.com',
    keywords=KEYWORDS,
    install_requires=REQUIREMENTS,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.mobilize.net/snowconvert/",
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Build Tools',
    ],
    python_requires='>=3.4',
)
