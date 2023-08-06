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
    'version': '0.1.2',
    'description': 'High performance asyncio REST client for polygon.io',
    'long_description': '# upoly\n\nAn Asyncio based, high performance, REST client libary for interacting\nwith the polygon REST api.\n\nRequires Python >=3.8,<=3.9\n\n## Installation\n\nThis library makes use of some high performance packages written in `C`/`Rust`\n(uvloop, orjson) so it may require `python-dev` on ubuntu or similar on\nother OS\'s.\n\n## Usage\n\nReccomend to create a copy of `./env.sample` as `./env`. Make sure `.env` is listed\nin `.gitignore`.\n\n```env\nPOLYGON_KEY_ID=REPACEWITHPOLYGONORALPACAKEYHERE\n```\n\nMany alternatives to `.env` exist. One such alternative is exporting\nlike so:\n\n```bash\n#!/bin/env bash\nexport POLYGON_KEY_ID=REPACEWITHPOLYGONORALPACAKEYHERE\n```\n\n```python\n# yourscript.py\nimport pytz\nfrom dotenv import load_dotenv\nimport pandas as pd\n\n# load Polygon key from .env file\nload_dotenv()\n# alternatively run from cli with:\n# POLYGON_KEY_ID=@#*$sdfasd python yourscript.py\n\n# Not recommend but can be set with os.environ["POLYGON_KEY_ID"] as well\n\nfrom upoly import async_polygon_aggs\n\n\nNY = pytz.timezone("America/New_York")\n\n# Must be a NY, pandas Timestamp\nstart = pd.Timestamp("2015-01-01", tz=NY)\nend = pd.Timestamp("2020-01-01", tz=NY)\n\ndf = async_polygon_aggs("AAPL", "minute", 1, start, end)\n```\n\n## TODO\n\n- [ ] unit tests\n- [ ] regression tests\n- [ ] integration tests\n- [ ] `/trade` endpoint functionality for tick data\n',
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
