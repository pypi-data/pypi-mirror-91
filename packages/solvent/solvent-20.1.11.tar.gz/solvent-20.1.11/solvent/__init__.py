import importlib
import pkgutil
import sys

from bullet import Bullet
import caffeine
import log
import pomace


def main(target=""):
    log.init()

    target = sys.argv[-1]

    package = importlib.import_module(__package__)
    modules = list(pkgutil.iter_modules(package.__path__))
    choices = [m.name for m in modules if not m.name.startswith("_")]

    cli = Bullet(prompt="\nSelect a script to run:", bullet=" ● ", choices=choices)
    if target not in choices:
        target = cli.launch()
        pomace.prompts.linebreak(force=True)

    module = importlib.import_module(f"{__package__}.{target}")

    caffeine.on(display=True)
    module.main()
