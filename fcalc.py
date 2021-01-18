# coding: utf8

import argparse

import FCALC
from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO, details = True)

parser = argparse.ArgumentParser()
parser.add_argument("-g","--option_gui", help = "Spécifie un fichier de config de l'apparence", action="store", default = "normal.gui")
args = parser.parse_args()

App = FCALC.Fcalc(url_help = 'https://github.com/FredThx/FCALC/wiki/Help', **vars(args))
App.run()
