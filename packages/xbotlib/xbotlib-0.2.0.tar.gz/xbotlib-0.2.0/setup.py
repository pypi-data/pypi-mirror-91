# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xbotlib']
install_requires = \
['slixmpp>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'xbotlib',
    'version': '0.2.0',
    'description': 'XMPP bots for humans',
    'long_description': '# xbotlib\n\n## XMPP bots for humans\n\n> status: experimental\n\nA friendly lightweight wrapper around\n[slixmpp](https://slixmpp.readthedocs.io/) for writing XMPP bots in Python. The\ngoal is to make writing and running XMPP bots easy and fun.\n\n`xbotlib` is a [single file implementation](./xbotlib.py) which can easily be\nunderstood and extended. It provides a small API surface which reflects the\n`slixmpp` way of doing things.\n\n## Install\n\n```sh\n$ pip install xbotlib\n```\n\n## Example\n\n```python\nfrom xbotlib import Bot\n\nclass EchoBot(Bot):\n    def react(self, message):\n        if message.type == "chat":\n          self.reply(to=message.sender, body=message.body)\n\nMyBot()\n```\n\nAnd then `python echo.py`. You will be asked a few questions like which account\ndetails your bot will be using. This will generate a `bot.conf` file in the\nsame working directory for further use.\n\n## More Examples\n\n- **[EchoBot](./examples/echo.py)**: Sends back what you sent it\n- **[WhisperBot](./examples/whisper.py)**: Pseudo-anonymous whispering in group chats\n\nSee the [examples](./examples/) directoy for all listings.\n\n## API Reference\n\nYour bot always sub-classes the `Bot` class provided from `xbotlib`. All\nunderling functions can be extended. For example, if you want to enable more\nplugins or add different functionality. If something feels awkwardthen please\nraise a ticket for that. Seamlessness is still a bitch but we\'re trying anyway.\n\n### Bot.react\n\nA function which you define in your bot implementation in order to respond to\nchat messages. You can respond to both direct messages and group chat messages\nin this function by checking the `message.type` which can be either `chat` or\n`groupchat`.\n\nArguments:\n\n- **message**: sent message and metadata (see [message](#message) reference below)\n\n### Bot.reply\n\nSend back a response to a direct chat message.\n\nArguments:\n\n- **to**: which user account to reply to (direct chat)\n- **room**: which room to reply to (group chat)\n- **body**: the message to send\n\n### Message\n\nA simple message format.\n\nAttributes:\n\n- **body**: the body of the message\n- **sender**: the sender of the message\n- **receive**: the receive of the message\n- **nickname**: the nickname of the sender\n- **type**: the type of message (`chat` or `groupchat`)\n\n## Roadmap\n\n- The library only handles reactions. The bots can only send messages when they\n  receive a message. It would be nice to allow for sending messages at specific\n  times.\n\n- Extend the `bot.conf` to allow for multiple bot configurations.\n\n- Sort out something for how to deploy them. It\'s easy to run them locally but\n  hard to run them on a server. Maybe something can be done for that as well.\n\n## Changes\n\nSee the [CHANGELOG.md](./CHANGELOG.md).\n\n## License\n\nSee the [LICENSE](./LICENSE.md).\n',
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
