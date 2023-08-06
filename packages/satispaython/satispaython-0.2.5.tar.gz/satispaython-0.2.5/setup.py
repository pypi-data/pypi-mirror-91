# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['satispaython']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.3.1,<4.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'satispaython',
    'version': '0.2.5',
    'description': 'A simple library to manage Satispay payments following the Web-button flow.',
    'long_description': "# satispaython\n\nA simple library to manage Satispay payments following the [Web-button flow](https://developers.satispay.com/docs/web-button-pay).\n\n## Requirements\n\n* python >= 3.8\n* [`cryptography`](https://github.com/pyca/cryptography) >= 3.2\n* [`requests`](https://github.com/psf/requests) >= 2.24\n\n## Installation\n\nYou can install this package with pip: `pip install satispaython`.\n\n## Usage\n\n### Key generation\n\nFirs of all you need a RSA private key. You may generate the key by yourself or you may use the provided utility functions:\n\n```python\nfrom satispaython.utils import generate_key, write_key\n\nrsa_key = generate_key()\nwrite_key(rsa_key, 'path/to/file.pem')\n```\n\nIn order to load the key from a PEM encoded file you may use the utility function:\n\n```python\nfrom satispaython.utils import load_key\n\nrsa_key = load_key('path/to/file.pem')\n```\n\n> :information_source: The function `write_key` stores the key in the PEM format. If you generate the key with any other method and you would like to use the `load_key` function, please make sure the key is stored within a file in the PEM format.\n\n> :information_source: Satispaython key management is based on [`cryptography`](https://cryptography.io/en/latest/) so all the functions which require an RSA key parameter expect an object of the class [`RSAPrivateKey`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey). If you don't use the `load_key` function then make sure your key is an instance of [`RSAPrivateKey`](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey).\n\nYou may protect your key with a password simply adding the `password` parameter:\n\n```python\nwrite_key(rsa_key, 'path/to/file.pem', password='mypassword')\nrsa_key = load_key('path/to/file.pem', password='mypassword')\n```\n\n### Satispay API\n\nSatispaython web requests are based on [`requests`](https://requests.readthedocs.io/en/master/) so the following functions return an instance of [`Response`](https://requests.readthedocs.io/en/latest/api/#requests.Response). On success, the Satispay API responds with a JSON encoded body, so you can simply check for the [`response.status_code`](https://requests.readthedocs.io/en/latest/api/#requests.Response.status_code) and eventually get the content with [`response.json()`](https://requests.readthedocs.io/en/latest/api/#requests.Response.json).\n\n> :information_source: If you need to use the Sandbox endpoints be sure to read the [section](https://github.com/otto-torino/satispaython#sandbox-endpoints).\n\nIn order to use the [Satispay API](https://developers.satispay.com/reference) simply import satispaython:\n\n```python\nimport satispaython as satispay\n```\n\nThen you can:\n\n#### Obtain a key-id using a token\n\n```python\nresponse = satispay.obtain_key_id(rsa_key, token)\n```\n\n> :information_source: The token is the activation code that can be generated from the Satispay Dashboard (or provided manually for Sandbox account).\n\n> :warning: Tokens are disposable! The key-id should be saved right after its creation.\n\n#### Make an authentication test\n\n```python\nresponse = satispay.test_authentication(key_id, rsa_key)\n```\n\n> :information_source: Authentication tests work on [Sandbox](https://developers.satispay.com/docs/sandbox-account) endpoints only.\n\n#### Create a payment\n\n```python\nresponse = satispay.create_payment(key_id, rsa_key, amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None)\n```\n\nYou may use the utility function `format_datetime` to get a correctly formatted `expiration_date` to supply to the request:\n\n```python\nfrom datetime import datetime, timezone, timedelta\nfrom satispaython.utils import format_datetime\n\nexpiration_date = datetime.now(timezone.utc) + timedelta(hours=1)\nexpiration_date = format_datetime(expiration_date)\n```\n\n#### Get payment details\n\n```python\nresponse = satispay.get_payment_details(key_id, rsa_key, payment_id)\n```\n\n### Sandbox endpoints\n\nBy default satispaython uses the production Satispay API. If you need to use the [Sandbox](https://developers.satispay.com/docs/sandbox-account) endpoints, simply set the `staging` parameter to `True`:\n\n```python\nresponse = satispay.obtain_key_id(rsa_key, token, staging=True)\nresponse = satispay.create_payment(key_id, rsa_key, amount_unit, currency, callback_url, expiration_date=None, external_code=None, metadata=None, idempotency_key=None, staging=True)\nresponse = satispay.get_payment_details(key_id, rsa_key, payment_id, staging=True)\n```\n",
    'author': 'Daniele Pira',
    'author_email': 'daniele.pira@otto.to.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/otto-torino/satispaython',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
