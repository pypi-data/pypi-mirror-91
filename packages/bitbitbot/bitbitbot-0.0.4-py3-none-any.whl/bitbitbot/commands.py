import pkgutil
from os import mkdir

from pathlib import Path

COMMANDS: dict[str, callable] = {}


def register(command_name: str) -> None:
    def _func_wrapper(func: callable):
        COMMANDS[command_name] = func
    return _func_wrapper


def discover_commands():
    plugins_path = Path('plugins')
    try:
        mkdir(plugins_path)
    except FileExistsError:
        pass

    for child in plugins_path.iterdir():
        if child.is_dir():
            mod_infos = pkgutil.walk_packages(
                [child.absolute()],
                '.'.join(child.parts) + '.'
            )
            for __, name, __ in mod_infos:
                __import__(name, fromlist=['_trash'])
