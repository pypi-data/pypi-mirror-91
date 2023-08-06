import re
from setuptools import setup, find_packages

long_description = """
Pure Python Pillow package wrapper.
"""

# Retrieve version number
VERSIONFILE = "PillowImage/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE))

setup(
    install_requires=[
        'reportlab>=3.5.19',
        'Pillow>=7.0',
        'PyBundle>=1.0.6',
    ],
    name='PillowImage',
    version=verstr,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/mrstephenneal/PillowImage',
    license='',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='Pillow wrapper for quick image alterations.',
    long_description=long_description,
)
