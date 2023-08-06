# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tls', 'tls.messaging', 'tls.messaging.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tls.messaging',
    'version': '0.1.5',
    'description': 'SDK for the Telstra Messaging API',
    'long_description': '# Telstra Messaging\n\nThe SDK for the Telstra messaging API.\n\n## Installing\n\n```bash\npip install tls.messaging\n```\n\n## Getting Started\n\nSet the `TLS_CLIENT_KEY` and `TLS_CLIENT_SECRET` environment variables. These\nare the `Client key` and `Client secret` you can find here:\n<https://dev.telstra.com/user/me/apps>.\n\nTo send your first SMS:\n\n```python\nfrom tls.messaging import sms\n\nsms.send(to="+61412345678", body="Hi")\n```\n\nTo set the required environment variables if your application is in `app.py`:\n\n```bash\nTLS_CLIENT_KEY="<client key>" TLS_CLIENT_SECRET="<client secret>" python app.py\n```\n\n## Authentication\n\nOn top of the authentication through the `TLS_CLIENT_KEY` and\n`TLS_CLIENT_SECRET` environment variables, authentication through code is also\nsupported. For example:\n\n```python\nfrom tls.messaging.utils.config import CONFIG\n\nCONFIG.tls_client_key = \'<client key>\'\nCONFIG.tls_client_secret = \'<client secret>\'\n```\n\n## Subscription\n\nFor more information, please see here:\n<https://dev.telstra.com/content/messaging-api#tag/Provisioning>.\n\n### Create Subscription\n\nFor more information, please see here:\n<https://dev.telstra.com/content/messaging-api#operation/createSubscription>.\n\nThe function `tls.messaging.subscription.create` can be used to create a\nsubscription. It takes the following arguments:\n\n- `active_days`: The number of days the subscription will be active.\n\nIt returns an object with the following properties:\n\n- `destination_address`: The phone number that a message can be sent to.\n- `active_days`: The number of days left on the subscription.\n\n### Get Subscription\n\nFor more information, please see here:\n<https://dev.telstra.com/content/messaging-api#operation/getSubscription>.\n\nThe function `tls.messaging.subscription.get` can be used to get the current\nsubscription. It takes no arguments. It returns an object with the following\nproperties:\n\n- `destination_address`: The phone number that a message can be sent to.\n- `active_days`: The number of days left on the subscription.\n\n### Delete Subscription\n\nFor more information, please see here:\n<https://dev.telstra.com/content/messaging-api#operation/deleteSubscription>.\n\nThe function `tls.messaging.subscription.delete` can be used to delete the current\nsubscription. It takes no arguments.\n\n## SMS\n\nFor more information, please see here:\n<https://dev.telstra.com/content/messaging-api#tag/Messaging>.\n\n### Send SMS\n\nFor more information, please see here:\n<https://dev.telstra.com/content/messaging-api#operation/sendSms>.\n\nThe function `tls.messaging.sms.send` can be used to send SMS. It takes the\nfollowing arguments:\n\n- `to`: The destination address, expected to be a phone number of the form\n  `+614XXXXXXXX` or `04XXXXXXXX`.\n- `body`: The SMS to send.\n- `from_` (optional): An alphanumeric value which will appear as the sender.\n  Note that phone numbers are not supported amd the maximum length is 11\n  characters. Certain well know senders will be blocked.\n- `validity` (optional): How long the platform should attempt to deliver the\n  message for (in minutes).\n- `scheduled_delivery` (optional): How long the platform should wait before\n  attempting to send the message (in minutes).\n\nIt returns an object with the following properties:\n\n- `to`: The destination.\n- `delivery_status`: Whether the delivery has been completed.\n- `message_id`: Unique identifier.\n- `message_status_url`: URL to retrieve the current delivery status.\n',
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
