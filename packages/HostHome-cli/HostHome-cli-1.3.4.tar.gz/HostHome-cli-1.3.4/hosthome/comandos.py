# -*- coding: utf-8 -*-
"""HostHome-CLI ara login y empezara tu cli
Usage:
  hosthome empezar               [-v | --verbose]
  hosthome eliminar              [-v | --verbose]
Opciones:
  -h --help                      Muestra esta pantalla.
  -v --version                   Show version.
"""

from docopt import docopt
import platform
from termcolor import cprint
from warnings import warn
import sys, os, requests

from hosthome.version import VERSION as __version__
from hosthome.login import login

url = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]

def mirarSiUsuarioEsImbecil(s: str):
  if s == "":
    cprint("Pon un argumento valido", "red")
    sys.exit(1)

archivo = """
lenguage: tempLen
main: tempMain
instalacion: insTemp
cmdStart: tempCmdStart

----- ADVERTENCIA
NO MENTIR SOBRE LA INFORMACION SINO EL HOST SERA ELIMINADO
NO TOCAR NADA A NO SER QUE SEA NECESARIO

SI OCURRE UN ERROR PODEIS PONERLO AQUI (https://github.com/HostHome-of/python-CLI/issues)

- JS
TIENE QUE TENER UN SCRIPT LLAMADO "start" PARA QUE FUNCIONE
- PYTHON
TIENE QUE TENER UN "requirements.txt" EN EL DIRECTORIO PADRE
- RUBY
TIENE QUE TENER UN Gemfile
-----
"""

def cojerInstalacion(lang: str, main: str):
  lenguages = {
    "ruby": ["bundle install", f"ruby {main}"],
    "npm": ["npm i", "npm start"],
    "php": ["none", f"php {main}"]
  } # Ayuda con los otros

  try:
    return lenguages[lang]
  except:
    return ["none", "none"]

def crearArchivo(main: str, lang: str):
  try:
    data = open(".host.home", "x")
  except:
    os.remove(".host.home")
    data = open(".host.home", "x")
  archivo2 = str(archivo.replace("tempLen", lang)
                .replace("tempMain", main)
                .replace("insTemp", cojerInstalacion(lang, main)[0])
                .replace("tempCmdStart", cojerInstalacion(lang, main)[1])
                )
  data.write(archivo2)

def main():

  try:
    args = docopt(__doc__, version="HostHome-CLI | version :: {}".format(__version__))

    if platform.system() != "Windows":
      warn("Encontré un sistema que no es Windows. Es posible que la instalación del paquete no funcione.")

    if args["empezar"]:
      data = login()
      cprint(f"> Hola {data['nombre']}", "green")
      main = input("Pon el archivo relativo en el que este el archivo \"main\" :: ")
      mirarSiUsuarioEsImbecil(main)
      idioma = input(f"Pon el idioma en el que esta (ruby|python|nodejs|scala|clojure|cs|php) MIRAR DOCS URGENTE ({url}docs) :: ").strip()
      mirarSiUsuarioEsImbecil(idioma)

      crearArchivo(main, idioma)

      sys.exit(0)
  except Exception as e:
    print(e)