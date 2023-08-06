# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_elements',
 'pytest_elements.common',
 'pytest_elements.decorators',
 'pytest_elements.elements',
 'pytest_elements.helpers',
 'pytest_elements.page_objects']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.3b0,<20.0',
 'deprecation>=2.0.7,<3.0.0',
 'faker>=4.0,<5.0',
 'mypy>=0.720,<0.721',
 'paramiko>=2.7.1,<3.0.0',
 'pydoc-markdown>=2.1.3,<3.0.0',
 'pymysql>=0.9.3,<0.10.0',
 'pytest-recordings>=0.4,<0.5',
 'pytest>=5.4,<6.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'pytest-elements',
    'version': '0.8',
    'description': 'Tool to help automate user interfaces',
    'long_description': None,
    'author': 'Jonah Caruso',
    'author_email': 'jayc035@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
