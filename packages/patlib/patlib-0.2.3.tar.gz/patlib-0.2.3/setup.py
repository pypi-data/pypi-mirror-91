# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patlib']

package_data = \
{'': ['*']}

install_requires = \
['ipdb', 'ipython', 'jedi<0.18', 'line_profiler', 'pdbpp', 'pudb']

setup_kwargs = {
    'name': 'patlib',
    'version': '0.2.3',
    'description': 'A collection of tools developed in conjunction with DAPPER.',
    'long_description': '# patlib\n\nA collection of tools developed in conjunction with DAPPER.\n',
    'author': 'patricknraanes',
    'author_email': 'patrick.n.raanes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
