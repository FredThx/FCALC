# coding: utf8

import FCALC
from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO, details = True)

App = FCALC.Fcalc(url_help = 'https://github.com/FredThx/FCALC/wiki/Help')
App.run()
