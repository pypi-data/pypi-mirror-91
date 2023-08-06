#!/usr/bin/env python3

import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name="makerchip-app",
    version="1.0.0",
    author="Redwood EDA",
    author_email="makerchip-app@redwoodeda.com",
    description="Makerchip desktop app",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url="https://gitlab.com/rweda/makerchip-app",
    packages=['makerchip'],
    classifiers = [
        "Topic :: Text Editors :: Integrated Development Environments (IDE)",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={'console_scripts': ['makerchip=makerchip:run']},
    install_requires=['requests', 'psutil', 'native_web_app', 'click', 'humanize'],
    python_requires='>=3.6'
)
