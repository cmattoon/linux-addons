#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    print("Install python-setuptools: sudo apt-get install python-setuptools")
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
    'bin/alphabetize',
    'bin/coderotate'
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
