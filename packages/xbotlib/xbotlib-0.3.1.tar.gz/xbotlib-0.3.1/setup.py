# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xbotlib']
install_requires = \
['slixmpp>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'xbotlib',
    'version': '0.3.1',
    'description': 'XMPP bots for humans',
    'long_description': '# xbotlib\n\n[![PyPI version](https://badge.fury.io/py/xbotlib.svg)](https://badge.fury.io/py/xbotlib)\n[![Build Status](https://drone.autonomic.zone/api/badges/decentral1se/xbotlib/status.svg?ref=refs/heads/main)](https://drone.autonomic.zone/decentral1se/xbotlib)\n\n## XMPP bots for humans\n\n> status: experimental\n\nA friendly lightweight wrapper around\n[slixmpp](https://slixmpp.readthedocs.io/) for writing XMPP bots in Python. The\ngoal is to make writing and running XMPP bots easy and fun. `xbotlib` is a\n[single file implementation](./xbotlib.py) which can easily be understood and\nextended. It provides a small API surface which reflects the `slixmpp` way of\ndoing things.\n\n## Install\n\n```sh\n$ pip install xbotlib\n```\n\n## Example\n\nPut the following in a `echo.py` file.\n\n```python\nfrom xbotlib import Bot\n\nclass EchoBot(Bot):\n    def react(self, message):\n        if message.type == "chat":\n          self.reply(message.body, to=message.sender)\n\nMyBot()\n```\n\nAnd then `python echo.py`. You will be asked a few questions like which account\ndetails your bot will be using.\n\nThis will generate a `bot.conf` file in the same working directory for further use.\n\n## More Examples\n\n- **[EchoBot](./examples/echo.py)**: Sends back what you sent it\n- **[WhisperBot](./examples/whisper.py)**: Pseudo-anonymous whispering in group chats\n\nSee the [examples](./examples/) directoy for all listings.\n\n## API Reference\n\nYour bot always sub-classes the `Bot` class provided from `xbotlib`. All\nunderling functions can be extended. For example, if you want to enable more\nplugins or add different functionality. If something feels awkward then please\nraise a ticket for that. Seamlessness is still a bitch but we\'re trying anyway.\n\n> Bot.react(message)\n\nA function which you define in your bot implementation in order to respond to\nchat messages. You can respond to both direct messages and group chat messages\nin this function by checking the `message.type` which can be either `chat` or\n`groupchat`.\n\nArguments:\n\n- **message**: sent message and metadata (see [message](#message) reference below)\n\n> Bot.reply(body, to=None, room=None)\n\nSend back a response to a direct chat message.\n\nArguments:\n\n- **body**: the message to send\n- **to**: which user account to reply to (direct chat)\n- **room**: which room to reply to (group chat)\n\n> EasyMessage\n\nA simple message format. This is the type that you work with when your function\naccepts a `message` argument.\n\nAttributes:\n\n- **body**: the body of the message\n- **sender**: the sender of the message\n- **receive**: the receive of the message\n- **nickname**: the nickname of the sender\n- **type**: the type of message (`chat` or `groupchat`)\n\n## Configure your bot\n\n### Using the environment\n\nYou can pass the `--no-input` option to your script invocation (e.g. `python bot.py --no-input`).\n\n`xbotlib` will try to read the following configuration values from the environment.\n\n- **XBOT_JID**\n- **XBOT_PASSWORD**\n- **XBOT_ROOM**\n- **XBOT_NICK**\n\n## Roadmap\n\nSee the [issue tracker](https://git.autonomic.zone/decentral1se/xbotlib/issues).\n\n## Changes\n\nSee the [CHANGELOG.md](./CHANGELOG.md).\n\n## License\n\nSee the [LICENSE](./LICENSE.md).\n',
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
