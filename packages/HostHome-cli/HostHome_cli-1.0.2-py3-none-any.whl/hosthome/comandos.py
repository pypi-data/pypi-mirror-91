# -*- coding: utf-8 -*-
"""HostHome-CLI ara login y empezara tu cli
Usage:
  hosthome empezar               (-v | --verbose)
  hosthome eliminar              (-v | --verbose)    
Opciones:
  -h --help                      Muestra esta pantalla.
  -v --version                   Show version.
"""

from docopt import docopt
import platform
from termcolor import cprint
from warnings import warn
import sys

from hosthome.version import VERSION as __version__
from hosthome.login import login


def main():

    args = docopt(__doc__, version="HostHome-CLI | version :: {}".format(__version__))

    print(args)

    if platform.system() != "Windows":
        warn("Encontré un sistema que no es Windows. Es posible que la instalación del paquete no funcione.")

    if args["empezar"]:
        estado = login()
        print(estado)
        sys.exit(0)