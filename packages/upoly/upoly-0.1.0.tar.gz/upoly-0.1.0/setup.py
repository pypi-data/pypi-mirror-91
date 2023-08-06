# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['upoly']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2,brotli]>=0.16.1,<0.17.0',
 'joblib>=1.0.0,<2.0.0',
 'nest-asyncio>=1.4.3,<2.0.0',
 'numpy>=1.19.5,<2.0.0',
 'orjson>=3.4.6,<4.0.0',
 'pandas-market-calendars>=1.6.1,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'uvloop>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'upoly',
    'version': '0.1.0',
    'description': 'High performance asyncio REST client for polygon.io',
    'long_description': "# upoly\n\nAn Asyncio based, high performance client libary for interacting\nwith the polygon REST api.\n\n## Installation\n\nThis library makes use of some high performance packages written in `C`/`Rust`\n(uvloop, orjson) so it may require `python-dev` on ubuntu or similar on\nother OS's.\n\n## Usage\n\ncreate a copy of `./env.sample` as `./env`\n\n## TODO\n\n- [ ] unit tests\n- [ ] regression tests\n- [ ] integration tests\n- [ ] `/trade` endpoint functionality for tick data\n",
    'author': 'Riley',
    'author_email': 'rileymshea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
