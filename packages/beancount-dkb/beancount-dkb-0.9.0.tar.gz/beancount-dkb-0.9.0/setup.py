# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_dkb']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'beancount-dkb',
    'version': '0.9.0',
    'description': 'Beancount Importer for DKB CSV exports',
    'long_description': "# Beancount DKB Importer\n\n[![image](https://github.com/siddhantgoel/beancount-dkb/workflows/beancount-dkb/badge.svg)](https://github.com/siddhantgoel/beancount-dkb/workflows/beancount-dkb/badge.svg)\n\n[![image](https://img.shields.io/pypi/v/beancount-dkb.svg)](https://pypi.python.org/pypi/beancount-dkb)\n\n[![image](https://img.shields.io/pypi/pyversions/beancount-dkb.svg)](https://pypi.python.org/pypi/beancount-dkb)\n\n[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n`beancount-dkb` provides an Importer for converting CSV exports of [DKB]\n(Deutsche Kreditbank) account summaries to the [Beancount] format.\n\n## Installation\n\n```sh\n$ pip install beancount-dkb\n```\n\nIn case you prefer installing from the Github repository, please note that\n`master` is the development branch so `stable` is what you should be installing\nfrom.\n\n## Usage\n\nIf you're not familiar with how to import external data into Beancount, please\nread [this guide] first.\n\nAdjust your [config file] to include `ECImporter` and `CreditImporter`\n(depending on what account you're trying to import).\n\nA sample configuration might look like the following:\n\n```python\nfrom beancount_dkb import ECImporter, CreditImporter\n\nIBAN_NUMBER = 'DE99 9999 9999 9999 9999 99' # your real IBAN number\n\nCARD_NUMBER = '9999 9999 9999 9999'         # your real Credit Card number\n\nCONFIG = [\n    ECImporter(\n        IBAN_NUMBER,\n        'Assets:DKB:EC',\n        currency='EUR',\n        file_encoding='utf-8',\n    ),\n\n    CreditImporter(\n        CARD_NUMBER,\n        'Assets:DKB:Credit',\n        currency='EUR',\n        file_encoding='utf-8',\n    )\n]\n```\n\nOnce this is in place, you should be able to run `bean-extract` on the command\nline to extract the transactions and pipe all of them into your Beancount file.\n\n```sh\n$ bean-extract /path/to/config.py transaction.csv >> you.beancount\n```\n\n## FAQ\n\n```sh\nERROR:root:Importer beancount_dkb.ec.ECImporter.identify() raised an unexpected error: 'utf-8' codec can't decode byte 0xf6 in position 17: invalid start byte\n```\n\nChange the `file_encoding` parameter. It seems like the CSV\nexports are `ISO-8859-1` encoded, but `utf-8`\nseems like a useful default.\n\n## Contributing\n\nContributions are most welcome!\n\nPlease make sure you have Python 3.6+ and [Poetry] installed.\n\n1. Clone the repository: `git clone https://github.com/siddhantgoel/beancount-dkb`\n2. Install the packages required for development: `poetry install`\n3. That's basically it. You should now be able to run the test suite: `poetry run py.test`.\n\n[Beancount]: http://furius.ca/beancount/\n[config file]: https://beancount.github.io/docs/importing_external_data.html#configuration\n[DKB]: https://www.dkb.de\n[Poetry]: https://python-poetry.org/\n[this guide]: https://beancount.github.io/docs/importing_external_data.html\n",
    'author': 'Siddhant Goel',
    'author_email': 'me@sgoel.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/siddhantgoel/beancount-dkb',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
