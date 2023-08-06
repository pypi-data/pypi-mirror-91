from setuptools import setup, find_packages
from setuptools.dist import get_metadata_version


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3' 
]

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='GradAnalystCodeTest',
    version='0.1.2',
    description='GradAnalystCodeTest is a python cli application that take a CSV file as a command argument with various options and manipulates data in various forms',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='Omar Jarkas',
    author_email='omarbjarkas@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='',
    entry_points = {
        'console_scripts': ['halfbricks=app.app:main'],
    },
    packages=find_packages(),
    install_requires=['argparse','PyInquirer','pyfiglet','matplotlib','pandas']

)