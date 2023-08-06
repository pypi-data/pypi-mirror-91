# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etch_a_tv']

package_data = \
{'': ['*']}

install_requires = \
['PyAudio>=0.2.11,<0.3.0',
 'numpy>=1.19.5,<2.0.0',
 'pygame-gui>=0.5.7,<0.6.0',
 'pygame>=2.0.1,<3.0.0',
 'scipy>=1.6.0,<2.0.0']

entry_points = \
{'console_scripts': ['etch_a_tv = etch_a_tv:__main__.main']}

setup_kwargs = {
    'name': 'etch-a-tv',
    'version': '0.1.0',
    'description': 'Draw images over the radio',
    'long_description': None,
    'author': 'Michaela',
    'author_email': 'git@michaela.lgbt',
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
