# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_imgproxy']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.1.0', 'djangorestframework>=3.9.0']

setup_kwargs = {
    'name': 'drf-imgproxy',
    'version': '1.0.0',
    'description': "Serialize Django's ImageField into imgproxy URLs for your Django REST\nFramework APIs to generate thumbnails.\n",
    'long_description': None,
    'author': 'VIPER Development UG',
    'author_email': 'info@viper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
