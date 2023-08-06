# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yap_styleguide']

package_data = \
{'': ['*']}

install_requires = \
['bandit>=1.7.0,<2.0.0',
 'black>=20.8b1,<21.0',
 'darglint>=1.5.8,<2.0.0',
 'flake8-annotations>=2.5.0,<3.0.0',
 'flake8-bandit>=2.1.2,<3.0.0',
 'flake8-black>=0.2.1,<0.3.0',
 'flake8-bugbear>=20.11.1,<21.0.0',
 'flake8-docstrings>=1.5.0,<2.0.0',
 'flake8-import-order>=0.18.1,<0.19.0',
 'flake8-isort>=4.0.0,<5.0.0',
 'flake8>=3.8.4,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0']}

setup_kwargs = {
    'name': 'yap-styleguide',
    'version': '0.0.2',
    'description': 'Yet another python styleguide',
    'long_description': '[![Tests](https://github.com/vahaah/yap-styleguide/workflows/Tests/badge.svg)](https://github.com/vahaah/yap-styleguide/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/vahaah/yap-styleguide/branch/master/graph/badge.svg)](https://codecov.io/gh/vahaah/yap-styleguide)\n[![PyPI](https://img.shields.io/pypi/v/yap-styleguide.svg)](https://pypi.org/project/yap-styleguide/)\n[![Read the Docs](https://readthedocs.org/projects/hypermodern-python/badge/)](https://yap-styleguide.readthedocs.io/)\n\n# Yet another python styleguide\n\n',
    'author': 'Alex Vakhitov',
    'author_email': 'alexius@hey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vahaah/yap-styleguide',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
