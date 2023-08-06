#!/usr/bin/env python

from sys import argv as ArgName
from getpass import getuser as EnvName

__all__ = ["hello"]

""" récupère la saisie utilisateur, contrôle sa longeur, ou choisi le nom de session"""
def cli(name=""):
    try:
        """ READme chapitre "pylint" pour des explications"""
        if len(ArgName) > 1:
            if len(ArgName[1]) > 16:
                name = "Long named Folk !"
            # READme chapitre "pylint" pour des explications
            else: # pylint: disable=W0702
                name = ArgName[1]

        else:
            name = EnvName()

    except:
        pass

    return name

""" fonction hello, récupère le prénom et le salue !"""
def hello():
    name = cli()
    return f"Hello {name}"
