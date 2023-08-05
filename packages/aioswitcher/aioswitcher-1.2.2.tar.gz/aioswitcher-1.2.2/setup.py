# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aioswitcher', 'aioswitcher.api', 'aioswitcher.bridge']

package_data = \
{'': ['*']}

extras_require = \
{'checkers': ['bandit==1.7.0',
              'black==20.8b1',
              'doc8==0.8.1',
              'flake8==3.8.4',
              'flake8-docstrings==1.5.0',
              'isort==5.7.0',
              'mypy==0.790',
              'pygments==2.7.3',
              'yamllint==1.25.0'],
 'tests': ['asynctest==0.13.0',
           'codecov==2.1.11',
           'pytest==6.2.1',
           'pytest-aiohttp==0.3.0',
           'pytest-asyncio==0.14.0',
           'pytest-cov==2.10.1',
           'pytest-sugar==0.9.4']}

setup_kwargs = {
    'name': 'aioswitcher',
    'version': '1.2.2',
    'description': 'Switcher Water Heater Unofficial Bridge and API.',
    'long_description': "# Switcher Water Heater Unofficial Bridge and API</br>[![pypi-version]][11] [![pypi-downloads]][11] [![license-badge]][4] [![conventional-commits]][0]\n\n[![gh-build-status]][7] [![read-the-docs]][8] [![codecov]][3]\n\nPyPi module named [aioswitcher][11] for integrating with the [Switcher Water Heater](https://www.switcher.co.il/).</br>\nPlease check out the [documentation][8].\n\n## Install\n\n```shell\npip install aioswitcher\n```\n\n## Usage Example\n\nPlease check out the [documentation][8] for the full usage section.\n\n```python\nasync with SwitcherV2Api(\n        your_loop, ip_address, phone_id,\n        device_id, device_password) as swapi:\n    # get the device state\n    state_response = await swapi.get_state()\n\n    # control the device: on / off / on + 30 minutes timer\n    turn_on_response = await swapi.control_device(consts.COMMAND_ON)\n    turn_off_response = await swapi.control_device(consts.COMMAND_OFF)\n    turn_on_30_min_response = await swapi.control_device(consts.COMMAND_ON, '30')\n```\n\n## Contributing\n\nThe contributing guidelines are [here](.github/CONTRIBUTING.md)\n\n## Code of Conduct\n\nThe code of conduct is [here](.github/CODE_OF_CONDUCT.md)\n\n<!-- Real Links -->\n[0]: https://conventionalcommits.org\n[2]: https://github.com/TomerFi/aioswitcher/releases\n[3]: https://codecov.io/gh/TomerFi/aioswitcher\n[4]: https://github.com/TomerFi/aioswitcher\n[7]: https://github.com/TomerFi/aioswitcher/actions?query=workflow%3ABuild\n[8]: https://aioswitcher.tomfi.info/\n[11]: https://pypi.org/project/aioswitcher\n<!-- Badges Links -->\n[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg\n[conventional-commits]: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg\n[gh-build-status]: https://github.com/TomerFi/aioswitcher/workflows/Build/badge.svg\n[license-badge]: https://img.shields.io/github/license/tomerfi/aioswitcher\n[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi&color=1082C2\n[pypi-version]: https://img.shields.io/pypi/v/aioswitcher?logo=pypi\n[read-the-docs]: https://readthedocs.org/projects/aioswitcher/badge/?version=stable\n",
    'author': 'Tomer Figenblat',
    'author_email': 'tomer.figenblat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/aioswitcher/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
