# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tls', 'tls.messaging', 'tls.messaging.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tls.messaging',
    'version': '0.1.3',
    'description': 'SDK for the Telstra Messaging API',
    'long_description': '# Telstra Messaging\n\nThe SDK for the Telstra messaging API.\n\n## Installing\n\n```bash\npip install messaging\n```\n\n## Getting Started\n\nSet the `TLS_CLIENT_KEY` and `TLS_CLIENT_SECRET` environment variables. These\nare the `Client key` and `Client secret` you can find here:\n<https://dev.telstra.com/user/me/apps>.\n\nTo send your first SMS:\n\n```python\nfrom tls.messaging import sms\n\nsms.send(to="+61412345678", body="Hi")\n```\n\n```bash\nTLS_CLIENT_KEY="XXXX" TLS_CLIENT_SECRET="YYYY" python app.py\n```\n',
    'author': 'David Andersson',
    'author_email': 'david-andersson@users.noreply.github.com ',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
