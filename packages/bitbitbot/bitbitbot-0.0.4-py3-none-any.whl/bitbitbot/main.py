from argparse import ArgumentParser
from os import getenv, mkdir
from pathlib import Path

from bitbitbot.bot import BitBitBot
from bitbitbot.commands import discover_commands

run_path = Path()
parser = ArgumentParser(
    prog='bitbitbot',
    description='A command line interface for the BitBitBot Twitch Chat Bot',
)
parser.set_defaults(func=lambda __: parser.print_help())
subparsers = parser.add_subparsers(help='subcommands')

# ============================================================================
# ===========================   RUN SUBPARSER   ==============================
# ============================================================================


def run(args):
    if args.name is None:
        print('ERROR: Missing required argument NAME')
        exit(1)
    if args.token is None:
        print('ERROR: Missing required argument TOKEN')
        exit(1)
    if args.channel is None:
        print('ERROR: Missing required argument CHANNEL')
        exit(1)

    discover_commands()
    bot = BitBitBot(
        username=args.name,
        token=args.token,
        channel=args.channel,
    )
    bot.start()


run_parser = subparsers.add_parser(
    'run',
    help='Run the chat bot',
)
run_parser.add_argument(
    '-n', '--name',
    default=getenv('BITBIT_NAME'),
    dest='name',
    help='The name of the account to use for the bot. Defaults to the BITBIT_NAME environment variable',
)
run_parser.add_argument(
    '-t', '--token',
    default=getenv('BITBIT_TOKEN'),
    dest='token',
    help='The oauth token for the bot. Defaults to the BITBIT_TOKEN environment variable',
)
run_parser.add_argument(
    '-c', '--channel',
    default=getenv('BITBIT_CHANNEL'),
    dest='channel',
    help='The twitch channel the bot should join. Defaults to the BITBIT_CHANNEL environment variable',
)
run_parser.set_defaults(func=run)

# ============================================================================
# ===========================   PLUGIN SUBPARSER   ==========================
# ============================================================================


def install(args):
    plugin_dir = Path('plugins')
    try:
        mkdir(plugin_dir)
    except FileExistsError:
        pass


plugin_parser = subparsers.add_parser(
    'plugin',
    help='Manage your plugins for the bot'
)
plugin_parser.set_defaults(func=lambda __: plugin_parser.print_help())
plugin_subparsers = plugin_parser.add_subparsers(help='plugin commands')

plugin_install_parser = plugin_subparsers.add_parser(
    'install',
    help='Install a plugin for the bot',
)
plugin_install_parser.set_defaults(func=install)

# ============================================================================
# ===========================   END SUBPARSERS  ==============================
# ============================================================================


def main():
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
