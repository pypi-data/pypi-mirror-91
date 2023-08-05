# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maestro', 'maestro.tests']

package_data = \
{'': ['*']}

install_requires = \
['pyusb>=1.1.0,<2.0.0']

extras_require = \
{'docs': ['Sphinx>=3.4.3,<4.0.0', 'sphinx-autodoc-annotation>=1.0-1,<2.0']}

setup_kwargs = {
    'name': 'maestro-servo',
    'version': '0.2.0',
    'description': 'A library for interacting with Pololu Maestro servo controllers',
    'long_description': "# Maestro server controller library\n\nThis library aims to support [Pololu's USB servo\ncontrollers](https://www.pololu.com/category/102/maestro-usb-servo-controllers),\nwhich can be used for servo control, and analogue input and output.\n\nMore information is available in [the\ndocumentation](https://maestro-servo.readthedocs.org/).\n",
    'author': 'Alex Dutton',
    'author_email': 'maestro@alexdutton.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexsdutton/python-maestro-servo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
