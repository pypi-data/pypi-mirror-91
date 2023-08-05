# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncpixel', 'asyncpixel.exceptions', 'asyncpixel.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'pydantic>=1.7.3,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'asyncpixel',
    'version': '1.0.0',
    'description': 'Asyncpixel',
    'long_description': '<p align="center">\n  <a href="https://obsidion-dev.com.com">\n    <img alt="Obsidion-dev" src="https://obsidion-dev.com/img/Bot%20Profile.png" width="60" />\n  </a>\n</p>\n<h1 align="center">\n  Asyncpixel\n</h1>\n\n<h3 align="center">\n  Easily access hypixel\'s api\n</h3>\n<p align="center">\n  Asyncpixel is an open source asyncronous python wrapper for the hypixel api with 100% of all endpoints.\n</p>\n\n<h3 align="center">\n 🤖 🎨 🚀\n</h3>\n\n<p align="center">\n  <a href="https://github.com/Obsidion-dev/asyncpixel/releases">\n    <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/Obsidion-dev/asyncpixel/total">\n  </a>\n  <a href="https://github.com/Obsidion-dev/asyncpixel/releases">\n    <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/Obsidion-dev/asyncpixel">\n  </a>\n  <a href="https://github.com/Obsidion-dev/asyncpixel/actions?workflow=Tests">\n  <img src="https://github.com/Obsidion-dev/asyncpixel/workflows/Tests/badge.svg" alt="Test status" />\n  </a>\n  <a href="https://discord.gg/rnAtymZnzH">\n    <img alt="Discord" src="https://img.shields.io/discord/695008516590534758">\n  </a>\n   <img src="https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg" alt="Code of conduct" />\n</p>\n\n<h3 align="center">\n  <a href="https://asyncpixel.readthedocs.org">Docs</a>\n  <span> · </span>\n  <a href="https://github.com/Obsidion-dev/asyncpixel/discussions?discussions_q=category%3AIdeas">Feature request</a>\n  <span> · </span>\n  <a href="https://github.com/Obsidion-dev/asyncpixel/issues">Report a bug</a>\n  <span> · </span>\n  Support: <a href="https://github.com/Obsidion-dev/asyncpixel/discussions">Discussions</a>\n  <span> & </span>\n  <a href="https://discord.gg/rnAtymZnzH">Discord</a>\n</h3>\n\n## ✨ Features\n\n- **Asyncronous.** Unlike other libraries Asyncpixel is fully asyncronous. This makes it perfect to use in your next discord bot or powerful website without having to worry about blocking.\n\n- **100% API coverage.** Asyncpixel is currently the only python library with full coverage of the hypixel API meaning that no endpoints are left untouched and outof your reach.\n\n- **Pydantic models.** All models are checked and validated by [Pydantic](https://github.com/samuelcolvin/pydantic) meaning that the data is always in the correct format perfect for you to use.\n\n- **Available on pypi.** Asyncpixel is available on pypi meaning no building from source just use `pip install asyncpixel` to use it in your project.\n\n## 🏁 Getting Started with Asyncpixel\n\nTo get started check out the documentation which [lives here](https://asyncpixel.readthedocs.org) and is generously hosted by readthedocs.\n\n### Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) or your favourite tool to install asyncpixel.\n\n```bash\npip install asyncpixel\n```\n\n### Example\n\n```python\nimport asyncpixel\nimport asyncio\n\nasync def main():\n    hypixel = asyncpixel.Hypixel("hypixel_api_key")\n    profile = await hypixel.profile("405dcf08b80f4e23b97d943ad93d14fd")\n    print(profile)\n    await hypixel.close()\n\n\nasyncio.run(main())\n```\n\n## ❗ Code of Conduct\n\nObsidion-dev is dedicated to providing a welcoming, diverse, and harrassment-free experience for everyone. We expect everyone in the Obsidion-dev community to abide by our [**Code of Conduct**](https://github.com/Obsidion-dev/asyncpixel/blob/master/CODE_OF_CONDUCT.rst). Please read it.\n\n## 🙌 Contributing to Asyncpixel\n\nFrom opening a bug report to creating a pull request: every contribution is appreciated and welcomed. If you\'re planning to implement a new feature or change the library please create an issue first. This way we can ensure your work is not in vain.\n\n### Not Sure Where to Start?\n\nA good place to start contributing, are the [Good first issues](https://github.com/Obsidion-dev/asyncpixel/labels/good%20first%20issue).\n\n## 📝 License\n\nAsyncpixel is open-source. The library is licensed [GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html).\n\n## 💬 Get in touch\n\nIf you have a question or would like to talk with other Asyncpixel users, please hop over to [Github discussions](https://github.com/Obsidion-dev/asyncpixel/discussions) or join our Discord server:\n\n[Discord chatroom](https://discord.gg/rnAtymZnzH)\n\n![Discord Shield](https://discordapp.com/api/guilds/695008516590534758/widget.png?style=shield)\n',
    'author': 'Darkflame72',
    'author_email': 'leon@bowie-co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Obsidion-dev/asyncpixel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
