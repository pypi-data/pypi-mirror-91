from argparse import ArgumentParser
from os import getenv

from bitbitbot.bot import BitBitBot


parser = ArgumentParser(
    prog='bitbitbot',
    description='Run BitBitBot Commands',
)

parser.add_argument(
    '-n', '--name',
    default=getenv('BITBIT_NAME'),
    dest='name',
    help='The name of the account to use for the bot. Defaults to the BITBIT_NAME environment variable',
)

parser.add_argument(
    '-t', '--token',
    default=getenv('BITBIT_TOKEN'),
    dest='token',
    help='The oauth token for the bot. Defaults to the BITBIT_TOKEN environment variable',
)

parser.add_argument(
    '-c', '--channel',
    default=getenv('BITBIT_CHANNEL'),
    dest='channel',
    help='The twitch channel the bot should join. Defaults to the BITBIT_CHANNEL environment variable',
)

args = parser.parse_args()

assert args.name is not None, 'Missing required argument NAME'
assert args.token is not None, 'Missing required argument TOKEN'
assert args.channel is not None, 'Missing required argument CHANNEL'

bot = BitBitBot(
    username=args.name,
    token=args.token,
    channel=args.channel,
)
bot.start()
