# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baidupcs_py',
 'baidupcs_py.app',
 'baidupcs_py.baidupcs',
 'baidupcs_py.commands',
 'baidupcs_py.common']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<9.0.0',
 'aget>=0.1.17,<0.2.0',
 'click>=7.1.2,<8.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.8.0,<10.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['BaiduPCS-Py = baidupcs_py.app:main']}

setup_kwargs = {
    'name': 'baidupcs-py',
    'version': '0.2.1',
    'description': 'Baidu Pcs App',
    'long_description': '# BaiduPCS-Py\n\nA BaiduPCS API and An App\n',
    'author': 'PeterDing',
    'author_email': 'dfhayst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PeterDing/BaiduPCS-Py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
