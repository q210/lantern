# coding: utf-8
import os

from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='ivideon-lantern',
    version='1.0.0',
    description='Ivideon lantern client from test task',
    long_description=(read('README.md') + '\n\n'),
    url='https://github.com/q210/lantern',
    license='MIT',
    author='Zaripov Timur',
    author_email='q210.frk@gmail.com',
    package_dir={'': 'src'},
    packages=find_packages(where='./src/'),
    scripts=['bin/lantern-app'],
    install_requires=['tornado'],
    include_package_data=True,
    classifiers=[
        'Private :: Do Not Upload',  # PyPI will not acknowledge this classifier hence
                                     # this package will not be uploaded by mistake
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
