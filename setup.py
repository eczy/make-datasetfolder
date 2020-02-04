import os
from glob import glob
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as fin:
    long_description = fin.read()

setup(
    name='make_datasetfolder',
    version='0.0.1',
    description='A utility to create a PyTorch DatasetFolder from any .csv or .tsv file with file path and class data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/eczy/make-datasetfolder',
    author='Evan Czyzycki',
    author_email='eczy3826@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5',
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'make-datasetfolder=main:main'
        ]
    }
)