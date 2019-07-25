##
#A command line tool to generate .gitignore files for your project
##
from setuptools import find_packages, setup
from scripts import *

dependencies = ['click', 'glob2']

setup(
    name='Sleepy',
    packages=find_packages(),
    version='0.1.0',
    url='https://github.com/benmshapiro/sleepy',
    download_url='',
    license='MIT',
    author='Ben Shapiro',
    author_email='benmshapiro@gmail.com',
    description='A commandline tool to generate .gitignore files for your project',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'goofy = scripts.cli:main',
        ],
    },
)
