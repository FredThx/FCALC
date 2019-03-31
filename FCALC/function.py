# coding: utf8

'''
Une fonction de la calculatrice
    avec
    - bouton
    - raccourcis clavier

'''
import tkinter as tkinter
from FCALC.fcalc_error import *
from FUTIL.my_logging import *

class Function(object):
    ''' A Fcal function
    '''
    def __init__(self, fcalc, function, nb_args = 1 ,bt_text = None, key = None, is_return = False, delete1car = True ):
        '''Initialisation
            - bt_parent     :   tkinter parent for buttons
            - nb_args       :   nb of args used in the stack
            - callback      :   the function
        '''
        self.nb_args = nb_args
        self.function = function
        self.fcalc = fcalc
        self.name = bt_text or key or "undefined"
        self.is_return = is_return
        self.delete1car = delete1car
        if bt_text:
            self.button = tkinter.Button(fcalc.buttons, text = bt_text, command = self._function)
            self.button.grid() #TODO : options
        if key:
            if not type(key)==list:
                key = [key]
            for k in key:
                fcalc.keys[k]=self

    def _function(self):
        '''The function called by the ui
            get nb_args in the stack
            put the result(s) in the stack
        '''
        logging.debug("Function %s called by %s"%(self.name, self))
        has_command_line = self.fcalc.command_line()
        if has_command_line:
            try:
                self.fcalc.stack.put(float(self.fcalc.command_line()))
                self.fcalc.v_command_line.set("")
            except ValueError as e:
                logging.info(e)
        if (not self.is_return) or (not has_command_line):
            try:
                if self.nb_args == "All":
                    args = self.fcalc.stack.get_all()
                else:
                    args = self.fcalc.stack.get(self.nb_args)
                self.fcalc.stack.put(self.function(*args))
            except Fcalc_error_stacktoosmall:
                logging.info("Not enought arguments.")
            except (ArithmeticError, ValueError) as e:
                logging.info(e)
                self.fcalc.stack.put(args)
