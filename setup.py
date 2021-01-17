#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path
readme_file = path.join(path.dirname(path.abspath(__file__)), 'README.md')

try:
    from m2r import parse_from_file
    readme = parse_from_file(readme_file)
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file) as f:
        readme = f.read()

setup(
    name='Pomodoro',
    version='1.2.0',
    url='https://github.com/KevinAp-5/Pomodoro',
    license='MIT License',
    author='KevinAp-5',
    author_email='keven.santos@protonmail.com',
    keywords='Pomodoro pomodoro pomodoro_clock TomatoTimer python_3.6.x',
    description='A simple way to use Pomodoro technique with python!',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['playsound', 'plyer'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
