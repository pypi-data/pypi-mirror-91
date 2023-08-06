# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apophis']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.5,<2.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'requests>=2.25.0,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['apophis = apophis.console:app']}

setup_kwargs = {
    'name': 'apophis',
    'version': '1.0.5',
    'description': 'Apophis: A python client for Kraken',
    'long_description': '[![Tests](https://github.com/tupui/apophis/workflows/Tests/badge.svg?branch=master)](\nhttps://github.com/tupui/apophis/actions?query=workflow%3A%22Tests%22\n)\n[![Code Quality](https://github.com/tupui/apophis/workflows/Code%20Quality/badge.svg?branch=master)](\nhttps://github.com/tupui/apophis/actions?query=workflow%3A%22Code+Quality%22\n)\n[![Package version](https://img.shields.io/pypi/v/apophis?label=pypi%20package)](\nhttps://pypi.org/project/apophis\n)\n\n# Apophis: A python client for Kraken\n\nApophis is a Python client for Kraken\'s REST API. It provides a common interface\nfor both *Kraken* and *Kraken Future*.\n\n**You want to say thanks?**\n\n<p align="center">\n<a href="https://www.buymeacoffee.com/tupui" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee: https://www.buymeacoffee.com/tupui" height=30" ></a>\n</p>\n\n## Quickstart\n\nPublic endpoints can be accessed without authentication.\n```python\nfrom apophis import Kraken\n\nwith Kraken() as exchange:\n    price = exchange.market_price(pair=\'XXRPZEUR\')\n    print(price)\n\n# 0.51081\n```\n\nFor placing orders, authentication is necessary:\n```python\nfrom apophis import Kraken\n\nkey = ...\nsecret = ...\nwith Kraken(key, secret) as exchange:\n    order = exchange.buy(pair=\'XXRPZEUR\', volume=1000, price=0.5)\n\n# Buying 1000 XXRPZEUR at 0.5 -> 500.0€\n```\n\nAlternatively, the low level API can be directly used to perform any kind of\nquery.\n\n```python\nfrom apophis import Apophis\n\nwith Apophis() as client:\n    response = client.query(\'Ticker\', {\'pair\': \'XXRPZEUR\'})\n    print(response[\'result\'])\n\n# {\'XXRPZEUR\': {\'a\': [\'0.48683000\', \'33129\', \'33129.000\'],\n#               \'b\': [\'0.48659000\', \'2915\', \'2915.000\'],\n#               \'c\': [\'0.48719000\', \'41.55695712\'],\n#               \'v\': [\'13015397.92184023\', \'46789050.96995769\'],\n#               \'p\': [\'0.48149626\', \'0.47328592\'],\n#               \'t\': [5110, 19079],\n#               \'l\': [\'0.45331000\', \'0.44697000\'],\n#               \'h\': [\'0.49354000\', \'0.49681000\'],\n#               \'o\': \'0.45730000\'}}\n```\n\nLast but not least, there is a fully functional CLI:\n```bash\n❯ apophis query Ticker pair=XXRPZEUR\n{\'error\': [], \'result\': {\'XXRPZEUR\': {\'a\': [\'0.45586000\', \'6356\', \'6356.000\'], \'b\': [\'0.45561000\', \'63000\', \'63000.000\'], \'c\': [\'0.45521000\', \'71.58800000\'], \'v\': [\'27100060.07361936\', \'45765330.64314690\'], \'p\': [\'0.43901689\', \'0.45396762\'], \'t\': [11527, 19747], \'l\': [\'0.41500000\', \'0.41500000\'], \'h\': [\'0.46588000\', \'0.49300000\'], \'o\': \'0.46153000\'}}}\n❯ apophis price "XXRPZEUR"\nXXRPZEUR: 0.45352\n```\n\n\n\n\n## Installation\n\nThe latest stable release (and older versions) can be installed from PyPI:\n\n    pip install apophis\n\nYou may instead want to use the development version from Github. Poetry is\nneeded and can be installed either from PyPI or:\n\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n\nThen once you cloned the repository, you can install it with:\n\n    poetry install\n\n## Contributing\n\nWant to add a cool logo, more doc, tests or new features? Contributors are more\nthan welcome! Feel free to open an [issue](https://github.com/tupui/apophis/issues)\nor even better propose changes with a [PR](https://github.com/tupui/apophis/compare).\nHave a look at the contributing guide.\n',
    'author': 'Pamphile Roy',
    'author_email': 'roy.pamphile@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tupui/apophis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
