# BitBitBot
An unopinionated, extensible Python ChatBot built for twitch on top of the [irc library](https://pypi.org/project/irc/). For more information, please refer to the documentation.

## Example Usage
```python
from bitbitbot.bot

bot = BitBitBot(
    {bot_account_name},         # bitbitbot
    {bot_oauth_token},          # oauth:123456890asdfgh
    {streamer_channel_name},    # metabytez
)

bot.start()
```
