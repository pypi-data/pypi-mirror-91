# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['custom_colormaps']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0', 'numpy>=1.19.5,<2.0.0']

setup_kwargs = {
    'name': 'custom-colormaps',
    'version': '0.3.2',
    'description': 'custom colormaps ',
    'long_description': "# custom colormaps\n\n[![PyPI](https://img.shields.io/pypi/v/demonstration.svg?label=PyPI&style=flat-square)](https://pypi.org/project/demonstration/)\n[![Python](https://img.shields.io/pypi/pyversions/demonstration.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/demonstration/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/python-package-template/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/python-package-template/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nThis package is a simple extension of matplotlib's colormaps with particular focus on the visualization of radio astronomical maps.\n\n## installation\n```\npip install custom-colormaps\n```\n\n## Usage\n\nclick custom_colormaps package ",
    'author': 'Rin Yamada',
    'author_email': 'yamada@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a-lab-nagoya/custom-colormaps',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
