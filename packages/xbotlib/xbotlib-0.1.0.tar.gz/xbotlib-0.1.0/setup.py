# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xbotlib']
install_requires = \
['slixmpp>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'xbotlib',
    'version': '0.1.0',
    'description': 'XMPP bots for humans',
    'long_description': "# xbotlib\n\n## XMPP bots for humans\n\nA friendly lightweight wrapper around [slixmpp](https://slixmpp.readthedocs.io/).\n\n`xbotlib` doesn't want to obscure the workings of the underlying library or\ninvent a totally new API. To this end, `xbotlib` is a [single file\nimplementation](./xbotlib.py) which can easily be understood and extended. It\nprovides a small API surface which reflects the `slixmpp` way of doing things.\n\nThe goal is to make writing and running XMPP bots in Python easy and fun.\n\n## Install\n\n```sh\n$ pip install xbotlib\n```\n\n## Example\n\n```python\nfrom xbotlib import Bot\n\nclass EchoBot(Bot):\n    def reply_direct_chat(self, message):\n        self.send_direct_chat(to=message.sender, body=message.body)\n\nMyBot()\n```\n\nAnd then `python echo.py`.\n\n## More Examples\n\n- **[EchoBot](./examples/echo.py)**: Sends back what you sent it\n- **[WhisperBot](./examples/whisper.py)**: Pseudo-anonymous whispering in group chats\n\nSee the [examples](./examples/) directoy for all listings.\n\n## API Reference\n\nYour bot always sub-classes the `Bot` class provided from `xbotlib`. All\nunderling functions can be extended. For example, if you want to enable more\nplugins or add different functionality. If something feels awkwardthen please\nraise a ticket for that. Seamlessness is still a bitch but we're trying anyway.\n\n### Bot.reply_direct_chat\n\nA function which you define in your bot implementation in order to respond to\ndirect chat messages.\n\nArguments:\n\n- **message**: sent message and metadata (see [message](#message) reference below)\n\n### Bot.send_direct_chat\n\nSend back a response to a direct chat message.\n\nArguments:\n\n- **to**: who to send it to (can be a user or a room)\n- **body**: the message to send\n\n### Bot.reply_group_chat\n\nA function which you define in your bot implementation in order to respond to\ngroup chat messages.\n\nArguments:\n\n- **message**: sent message and metadata (see [message](#message) reference below)\n\n### Bot.send_group_chat\n\nSend back a response to a group chat message.\n\nArguments:\n\n- **to**: who to send it to (can be a user or a room)\n- **body**: the message to send\n\n### Message\n\nA simple message format.\n\nAttributes:\n\n- **body**\n- **sender**\n- **receive**\n- **nickname**\n- **type**\n\n## Roadmap\n\n- The library only handles reactions. The bots can only send messages when they\n  receive a message. It would be nice to allow for sending messages at specific\n  times.\n\n- Extend the `bot.conf` to allow for multiple bot configurations.\n\n- Sort out something for how to deploy them. It's easy to run them locally but\n  hard to run them on server. Maybe something can be done for that as well.\n\n## Changes\n\nSee the [CHANGELOG.md](./CHANGELOG.md).\n\n## License\n\nSee the [LICENSE](./LICENSE.md).\n",
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
