# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyp_boy', 'pyp_boy.common.tools', 'pyp_boy.gui']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.32.1,<5.0.0',
 'RandomWords>=0.3.0,<0.4.0',
 'inspy-logger==2.0-a3',
 'inspyre-toolbox>=1.0a2,<2.0']

entry_points = \
{'console_scripts': ['pyp-boy = pyp_boy.main:run_gui']}

setup_kwargs = {
    'name': 'pyp-boy',
    'version': '1.0a2',
    'description': 'Python-based program to assist with Fallout hacking. With a GUI!',
    'long_description': None,
    'author': 'Taylor-Jayde Blackstone',
    'author_email': 't.blackstone@inspyre.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
