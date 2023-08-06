# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dorado',
 'dorado.sensitivity',
 'dorado.sensitivity.data',
 'dorado.sensitivity.tests']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml', 'synphot']

setup_kwargs = {
    'name': 'dorado-sensitivity',
    'version': '0.1.0',
    'description': 'Dorado sensitivity and exposure time calculator',
    'long_description': None,
    'author': 'Brad Cenko',
    'author_email': 'brad.cenko@nasa.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dorado-science/dorado-sensitivity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
