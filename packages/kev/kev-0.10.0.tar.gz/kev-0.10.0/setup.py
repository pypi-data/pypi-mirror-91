# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kev',
 'kev.backends',
 'kev.backends.redis',
 'kev.backends.s3',
 'kev.backends.s3redis',
 'kev.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.43,<2.0.0',
 'envs>=1.3,<2.0',
 'jupyterlab>=3.0.0,<4.0.0',
 'pyzmq==19.0.2',
 'redis>=3.5.3,<4.0.0',
 'valley>=1.5.5,<2.0.0']

setup_kwargs = {
    'name': 'kev',
    'version': '0.10.0',
    'description': 'K.E.V. (Keys, Extra Stuff, and Values) is a Python ORM for key-value stores and document databases based on Valley. Currently supported backends are Redis, S3 and a S3/Redis hybrid backend.',
    'long_description': None,
    'author': 'Brian Jinwright',
    'author_email': 'brian@ipoots.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
