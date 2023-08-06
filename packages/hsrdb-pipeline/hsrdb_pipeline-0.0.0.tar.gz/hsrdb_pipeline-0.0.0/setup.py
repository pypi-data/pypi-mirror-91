from setuptools import setup, find_packages
import os
import shutil


def readme():
    with open('README.md') as f:
        return f.read()


def requirements():
    """
    Create a list of packages from requirements.txt.
    Pop `setuptools`.
    :return:
    """
    with open('requirements.txt') as f:
        req = f.read().splitlines()
    for r in req:
        if r.startswith('setuptools'):
            req.remove(r)
    return req


if os.path.exists('hsrdb_pipeline.egg-info'):
    shutil.rmtree('hsrdb_pipeline.egg-info')

setup(
    name='hsrdb_pipeline',
    version='0.0.0',
    license='GPLv3',
    url='https://github.com/dtriand/hsrdb_pipeline',
    download_url='',
    # project_urls={
    #     'Bug Tracker': '',
    #     'Documentation': ''
    # },
    author='Dimitris Triandafillidis',
    author_email='dimitristriandafillidis@gmail.com',
    description='',
    long_description=readme(),
    keywords='',
    package_dir={"": "src"},
    packages=find_packages(
        where='src',
        exclude=['tests', 'tests.*']  # Do not include tests in distribution
    ),
    python_requires='>=3.8.5',
    install_requires=requirements(),
    # extras_require={}  # Specified in setup.cfg
    #     # Optional requirements. Install via pip install xtl[interactive]
    # },
    tests_require=['pytest'],
    package_data={
        # '': ['requirements.txt']
        # non-py files to include
        # specified in MANIFEST.in instead
    },
    entry_points={
        'console_scripts': [
            'hsrdb = hsrdb_pipeline.hi:say_hi'
        ]
    }
)
