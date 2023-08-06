# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tts_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.11.3',
 'google-cloud-texttospeech==2.2.0',
 'ibm-watson==4.3.0',
 'requests==2.22.0']

setup_kwargs = {
    'name': 'tts-wrapper',
    'version': '0.5.2',
    'description': 'A hassle-free Python library that allows one to use text-to-speech APIs with the same interface',
    'long_description': None,
    'author': 'Giulio Bottari',
    'author_email': 'giuliobottari@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
