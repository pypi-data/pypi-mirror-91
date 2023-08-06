from setuptools import setup, find_packages
import pathlib

with open('README.md', 'rt') as f:
    long_description = f.read()

setup(
    name='pytar',
    version='0.600',
    packages=find_packages(),
    url='https://github.com/Valmarelox/pytar',
    license='MIT',
    author='efi',
    author_email='valmarelox@gmail.com',
    description='pure python3.8 tar parsing (WIP)',
    zip_safe=False,
    python_requires='>=3.8',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
