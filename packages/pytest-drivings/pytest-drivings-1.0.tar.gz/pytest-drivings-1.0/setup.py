# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_drivings']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.3b0,<20.0',
 'deprecation>=2.0.7,<3.0.0',
 'mypy>=0.720,<0.721',
 'paramiko>=2.7.1,<3.0.0',
 'psutil>=5.6.7,<6.0.0',
 'pytest-xdist>=1.31.0,<2.0.0',
 'selenium-requests>=1.3,<2.0',
 'selenium>=3.141.0,<4.0.0']

entry_points = \
{'pytest11': ['pytest_webdriver = pytest_webdriver.webdriver']}

setup_kwargs = {
    'name': 'pytest-drivings',
    'version': '1.0',
    'description': 'Tool to allow webdriver automation to be ran locally or remotely',
    'long_description': None,
    'author': 'Jonah Caruso',
    'author_email': 'jayc035@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
