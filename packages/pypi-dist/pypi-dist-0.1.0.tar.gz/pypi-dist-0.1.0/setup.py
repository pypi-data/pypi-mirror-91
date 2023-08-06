import os
from setuptools import setup
from pathlib import Path

PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
VERSION_PATH = PROJECT_ROOT.joinpath(Path('.VERSION'))
README_PATH = PROJECT_ROOT.joinpath(Path('README.md'))

def read(file_name):
    if file_name.exists():
        with open(file_name) as f:
            return f.read()
    else:
        return None


setup(
    name='pypi-dist',
    version=read(VERSION_PATH) or '0.1.0',
    author='Patrick Ayoup',
    author_email='patrick.ayoup@gmail.com',
    url='https://github.com/patrickayoup/pypi-dist',
    description='Convenience script for distributing projects to PyPi',
    license='MIT',
    keywords='pypi',
    py_modules=['pypi_dist'],
    entry_points = {
        'console_scripts': ['pypi-dist=pypi_dist'],
    },
    install_requires=['gitpython',
                      'twine',
                      'semver',
                      'click',
                      'wheel',
                      'setuptools'],
    long_description=read(README_PATH),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
