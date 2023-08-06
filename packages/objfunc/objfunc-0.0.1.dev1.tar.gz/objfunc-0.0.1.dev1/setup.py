from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='objfunc',
    version='0.0.1.dev1',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.*',
    install_requires=[
        "typer",
    ],

    author='Minhwan Kim',
    author_email='minhwan.kim@member.fsf.org',
    description='Client for objfunc.com',
    keywords='client API',
    url='https://github.com/azurelysium/objfunc-cli',
    project_urls={
        'Documentation': 'https://github.com/azurelysium/objfunc-cli',
        'Source Code': 'https://github.com/azurelysium/objfunc-cli',
    },
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],

    long_description=long_description,
    long_description_content_type='text/markdown',

    entry_points={
        'console_scripts': [
            'objfunc = objfunc.cli:app',
        ],
    },
)
