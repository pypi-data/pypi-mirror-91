#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    instalacion de una nueva version

    CAMBIAR LA VERSION

    Crear una nueva distribuicion
    'python setup.py sdist bdist_wheel'

    Checkear si esta
    'twine check dist/*'
    Si esta la version todo ha salido bien

    Luego: 'twine upload --repository-url https://upload.pypi.org/legacy/ dist/maupip-VERSION*', version = ej: 1.0.3* 
    Para suvirlo. La version tiene que estar despues de dist/ con un asterisco al final (*)

    rellenar lo que te pregunte

    'pip uninstall mau' (Si esta instalado)
    'pip install mau', Le puedes dar al link que te saldra <- o -> instalarlo y ya

"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = []
f = open("./requirements.txt", "r").read().split("\n")
for r in f:
    requirements.append(str(r))


setup(
    name="HostHome-cli",
    version="1.0.2",
    description="HostHome-cli para empezar con el host",
    long_description=readme,
    author="Maubg",
    url="https://github.com/HostHome-of/python-CLI",
    include_package_data=True,
    install_requires=requirements,
    packages=[
        "hosthome",
    ],
    license="GNU",
    zip_safe=False,
    keywords="host, hosthome, maubg, python, py, hosty, hoster, home",
    entry_points={
        "console_scripts": ["hosthome=hosthome.comandos:main"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha", "Environment :: Console",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ])
