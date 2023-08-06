# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_webrtc']

package_data = \
{'': ['*']}

install_requires = \
['aiortc>=1.0.0', 'streamlit>=0.63']

setup_kwargs = {
    'name': 'streamlit-webrtc',
    'version': '0.3.0',
    'description': '',
    'long_description': '# streamlit-webrtc\n',
    'author': 'Yuichiro Tsuchiya',
    'author_email': 't.yic.yt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
