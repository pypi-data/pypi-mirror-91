# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['hbctool']
install_requires = \
['docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['hbctool = hbctool:main']}

setup_kwargs = {
    'name': 'hbctool',
    'version': '0.1.1',
    'description': 'A command-line interface for disassembling and assembling the Hermes Bytecode.',
    'long_description': "# hbctool \n\n[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://python.org) [![PyPI version](https://badge.fury.io/py/hbctool.svg)](https://badge.fury.io/py/hbctool) [![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](/LICENSE)\n\nA command-line interface for disassembling and assembling the Hermes Bytecode. \n\nSince React Native team created their own JavaScript engine (named Hermes) for running the React Native application, the JavaScript source code is compiled to the Hermes bytecode. In peneration test project, I found that some React Native applications have already been migrated to Hermes engine. It is really head for me to analyze or patch those applications. Therefore, I created this tool for helping any pentester to test the Hermes bytecode.\n\n> [Hermes](https://hermesengine.dev/) is an open-source JavaScript engine optimized for running React Native apps on Android. For many apps, enabling Hermes will result in improved start-up time, decreased memory usage, and smaller app size. At this time Hermes is an opt-in React Native feature, and this guide explains how to enable it.\n\n## Installation\n\nTo install hbctool, simply use pip:\n\n```\npip install hbctool\n```\n\n## Usage\n\nPlease execute `hbctool --help` for showing the usage.\n\n```\nhbctool --help   \nA command-line interface for disassembling and assembling\nthe Hermes Bytecode.\n\nUsage:\n    hbctool disasm <HBC_FILE> <HASM_PATH>\n    hbctool asm <HASM_PATH> <HBC_FILE>\n    hbctool --help\n    hbctool --version\n\nOperation:\n    disasm              Disassemble Hermes Bytecode\n    asm                 Assemble Hermes Bytecode\n\nArgs:\n    HBC_FILE            Target HBC file\n    HASM_PATH           Target HASM directory path\n\nOptions:\n    --version           Show hbctool version\n    --help              Show hbctool help manual\n\nExamples:\n    hbctool disasm index.android.bundle test_hasm\n    hbctool asm test_hasm index.android.bundle\n```\n\n> For Android, the HBC file normally locates at `assets` directory with `index.android.bundle` filename.\n\n## Contribution\n\nFeel free to create an issue or submit the merge request. Anyway you want to contribute this project. I'm very happy about it.\n\nHowever, please run the unittest before submit the pull request.\n\n```\npython test.py\n```\n\nI use poetry to build this tool, For building tool, simply execute:\n\n```\npoetry install\n```",
    'author': 'bongtrop',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
