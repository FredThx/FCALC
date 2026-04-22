# coding: utf8

import argparse

import FCALC
from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO, details = True)

parser = argparse.ArgumentParser()
parser.add_argument("-g","--option_gui",  help = "Spécifie un fichier de config de l'apparence", action="store", default = "normal.gui")
parser.add_argument("--check_update", dest = "check_update",help = "Vérification de l'existance d'une mise à jour.", action = 'store_true', default = True)
parser.add_argument("--no_check_update", dest = "check_update",help = "Vérification de l'existance d'une mise à jour.", action = 'store_false')
args = parser.parse_args()
print(args)
App = FCALC.Fcalc(url_help = 'https://github.com/FredThx/FCALC/wiki/Help', **vars(args))
App.run()
