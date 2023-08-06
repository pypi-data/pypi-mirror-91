# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tensorx', 'tensorx.train']

package_data = \
{'': ['*']}

install_requires = \
['numpy']

extras_require = \
{'matplotlib': ['matplotlib>=3.3.0,<4.0.0'],
 'pygraphviz': ['pygraphviz'],
 'pyqtgraph': ['pyqtgraph>=0.11.0,<0.12.0', 'PyQt5>=5.15.0,<6.0.0'],
 'tensornetwork': ['tensornetwork>=0.4.1,<0.5.0'],
 'tqdm': ['tqdm>=4.48.1,<5.0.0']}

setup_kwargs = {
    'name': 'tensorx',
    'version': '2.1.0',
    'description': 'TensorX is an open source library to build deep neural network models',
    'long_description': '## \n\n<p align="center">\n<img src="https://raw.githubusercontent.com/davidenunes/tensorx/master/docs/theme/assets/images/logo_full.svg" width="80%" alt="Tensor X Logo">\n</p>\n\n<p align="center">\n  <a href="http://www.apache.org/licenses/LICENSE-2.0.html">\n    <img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="Apache 2 Licence"/>\n  </a>\n  <a href="https://travis-ci.org/github/davidenunes/tensorx">\n    <img src="https://travis-ci.org/davidenunes/tensorx.svg" alt="Travis CI"/>\n  </a>\n  <a href="https://pypi.org/project/tensorx">\n    <img src="https://img.shields.io/pypi/v/tensorx.svg" alt="Python Package Index"/>\n  </a>\n  <a href="https://pypistats.org/packages/tensorx">\n    <img src="https://img.shields.io/pypi/dm/tensorx.svg" alt="Downloads"/>\n  </a>\n</p>\n\n\n**TensorX** is a high-level deep neural network library written in Python\nthat simplifies model specification, training, and execution using \n[TensorFlow](https://www.tensorflow.org/). It was designed for fast \nprototyping with minimum verbose and provides a set of modular \ncomponents with a user-centric consistent API.\n\n## Design Philosophy\n\nTensorX aims to be **simple but sophisticated** without a code base plagued by unnecessary abstractions and \nover-engineering and **without sacrificing performance**. It uses Tensorflow without hiding it completely behind a new namespace, it\'s mean to be a complement\ninstead of a complete abstraction. The design mixes functional **dataflow computation graphs** with **object-oriented** \nneural network **layer** building blocks that are **easy to add to and extend**. \n\n## Feature Summary\n\n* **Neural Network** layer building blocks like `Input`, `Linear`, `Lookup`;\n* **New TensorFlow ops**:  `gumbel_top`, `logit`, `sinkhorn`, etc;\n* **`Graph` Utils**: allow for validation and compilation of layer graphs;\n* **`Model` Class**: for easy _inference_, _training_, and _evaluation_;\n* **Training Loop**: easily customizable with a ``Callback`` system;\n\n## Installation\nTensorX is written in pure python but **depends on Tensorflow**, which needs to be installed from the `tensorflow` package.\nThe reason for this is that you might want to install Tensorflow builds optimized for your machine (see \n[these](https://github.com/davidenunes/tensorflow-wheels)). Additionally, TensorX has **optional\ndependencies** like `matplotlib` or `pygraphviz` for certain functionality.\n\n## Pip installation\nInstall using `pip` with the following commands:\n\n```shell\npip install tensorflow \npip install tensorx\n```\n\nFor more details about the installation, check the [documentation](https://tensorx.org/start/install/).\n\n## Test your installation\n```python\nimport tensorflow as tf\nimport tensorx as tx\n```\n\n\n## Documentation\nFor details about TensorX API, tutorials, and other documentation, see [https://tensorx.org](https://tensorx.org).\nYou can help by trying the project out, reporting bugs, suggest features, and by letting me know what you think. \nIf you want to help, please read the [contribution guide](https://tensorx.org/contributing/).\n\n\n## Author\n* **[Davide Nunes](https://github.com/davidenunes)**: get in touch [@davidelnunes](https://twitter.com/davidelnunes) \nor by [e-mail](mailto:davidenunes@pm.me)\n\n## License\n\n[Apache License 2.0](LICENSE)\n',
    'author': 'Davide Nunes',
    'author_email': 'davidenunes@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tensorx.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
