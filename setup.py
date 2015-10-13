#!/usr/bin/env python
from setuptools import setup
"""
If you only want to install some of the scripts, you can manually copy them
to the /bin/ or /usr/bin directory and make them executable (chmod +x).

You can also comment out lines in the 'scripts' list below:
"""
scripts = [
    'bin/ansi-colormap',
    'bin/icanhazip',
    'bin/wifipassword',
    #'bin/mint-post-install',
    'bin/whoamiv',
    'bin/cleanhosts',
    'bin/alphabetize'
    ]

config = {
    'name': 'Linux Addons',
    'author': 'Curtis Mattoon',
    'author_email': 'cmattoon@cmattoon.com',
    'scripts': scripts,
    'packages': [
        'lxlib'
        ]
}

setup(**config)
