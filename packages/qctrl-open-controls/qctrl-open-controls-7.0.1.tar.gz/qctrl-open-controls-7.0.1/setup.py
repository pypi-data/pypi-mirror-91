# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlopencontrols',
 'qctrlopencontrols.driven_controls',
 'qctrlopencontrols.dynamic_decoupling_sequences']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0', 'scipy>=1.3,<2.0', 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'qctrl-open-controls',
    'version': '7.0.1',
    'description': 'Q-CTRL Open Controls',
    'long_description': '# Q-CTRL Open Controls\n\nQ-CTRL Open Controls is an open-source Python package that makes it easy to\ncreate and deploy established error-robust quantum control protocols from the\nopen literature. The aim of the package is to be the most comprehensive library\nof published and tested quantum control techniques developed by the community,\nwith easy to use export functions allowing users to deploy these controls on:\n\n- Custom quantum hardware\n- Publicly available cloud quantum computers\n- The [Q-CTRL product suite](https://q-ctrl.com/products/)\n\nAnyone interested in quantum control is welcome to contribute to this project.',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.4,<3.9',
}


setup(**setup_kwargs)
