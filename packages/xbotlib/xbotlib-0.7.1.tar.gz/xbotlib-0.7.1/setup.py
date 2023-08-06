# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xbotlib']
install_requires = \
['slixmpp>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'xbotlib',
    'version': '0.7.1',
    'description': 'XMPP bots for humans',
    'long_description': '# xbotlib\n\n[![PyPI version](https://badge.fury.io/py/xbotlib.svg)](https://badge.fury.io/py/xbotlib)\n[![Build Status](https://drone.autonomic.zone/api/badges/decentral1se/xbotlib/status.svg?ref=refs/heads/main)](https://drone.autonomic.zone/decentral1se/xbotlib)\n\n## XMPP bots for humans\n\n> status: experimental\n\nA friendly lightweight wrapper around\n[slixmpp](https://slixmpp.readthedocs.io/) for writing XMPP bots in Python. The\ngoal is to make writing and running XMPP bots easy and fun. `xbotlib` is a\n[single file implementation](./xbotlib.py) which can easily be understood and\nextended. It provides a small API surface which reflects the `slixmpp` way of\ndoing things.\n\n## Install\n\n```sh\n$ pip install xbotlib\n```\n\n## Example\n\nPut the following in a `echo.py` file. `xbotlib` provides a number of example\nbots which you can use to get moving fast and try things out.\n\n```python\nfrom xbotlib import EchoBot\n\nEchotBot()\n```\n\nAnd then `python echo.py`. You will be asked a few questions like which account\ndetails your bot will be using.\n\nThis will generate a `bot.conf` file in the same working directory for further use.\n\nHere\'s the code for the `EchoBot`.\n\n```python\nclass EchoBot(Bot):\n    def direct(self, message):\n        self.reply(message.body, to=message.sender)\n\n    def group(self, message):\n        if "echobot" in message.body:\n            self.reply(message.body.split(":")[-1], room=message.room)\n```\n\nRead more in the [API reference](#api-reference) for how to write your own bots.\n\n## All examples\n\n- **EchoBot**: Sends back what you sent it\n- **WhisperBot**: Pseudo-anonymous whispering in group chats\n\nSee [xbotlib.py](./xbotlib.py) for all example bots.\n\n## API Reference\n\nWhen writing your own bot, you always sub-class the `Bot` class provided from\n`xbotlib`. Then if you want to respond to a direct message, you write a\n[direct](#botdirectmessage) function. If you want to respond to a group chat\nmessage, you write a [group](#botgroupmessage) function.\n\n### Bot.direct(message)\n\nRespond to direct messages.\n\nArguments:\n\n- **message**: received message (see [SimpleMessage](#simplemessage) below for available attributes)\n\n### Bot.group(message)\n\nRespond to a message in a group chat.\n\nArguments:\n\n- **message**: received message (see [SimpleMessage](#simplemessage) below for available attributes)\n\n### SimpleMessage\n\nA simple message interface.\n\nAttributes:\n\n- **body**: the body of the message\n- **sender**: the user the message came from\n- **room**: the room the message came from\n- **receiver**: the receiver of the message\n- **nickname**: the nickname of the sender\n- **type**: the type of message (`chat` or `groupchat`)\n\n## Configure your bot\n\n### Using the environment\n\nYou can pass the `--no-input` option to your script invocation (e.g. `python bot.py --no-input`).\n\n`xbotlib` will try to read the following configuration values from the environment.\n\n- **XBOT_JID**: The username of the bot account\n- **XBOT_PASSWORD**: The password of the bot account\n- **XBOT_NICK**: The nickname that the bot uses\n\n## Roadmap\n\nSee the [issue tracker](https://git.autonomic.zone/decentral1se/xbotlib/issues).\n\n## Changes\n\nSee the [CHANGELOG.md](./CHANGELOG.md).\n\n## License\n\nSee the [LICENSE](./LICENSE.md).\n',
    'author': 'decentral1se',
    'author_email': 'lukewm@riseup.net',
    'maintainer': 'decentral1se',
    'maintainer_email': 'lukewm@riseup.net',
    'url': 'https://git.autonomic.zone/decentral1se/xbotlib',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
