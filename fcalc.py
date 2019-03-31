# coding: utf8

import FCALC
from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = DEBUG, details = True)

App = FCALC.Fcalc()
App.run()
