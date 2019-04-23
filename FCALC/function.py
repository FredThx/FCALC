# coding: utf8

'''
Une fonction de la calculatrice
    avec
    - bouton
    - raccourcis clavier
'''
import tkinter as tkinter
import logging
import math

from .fcalc_error import *
from .stack_item import *
from .infobulle import *

class Function(object):
    ''' A Fcal function
    '''
    def __init__(self, fcalc, parent, function, nb_args = 1 ,bt_text = None, key = None, is_return = False, delete1car = True, label = None, description = None ):
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
        if key:
            if not type(key)==list:
                key = [key]
            for k in key:
                fcalc.keys[k]=self
        self.label = label or bt_text or key[0] or "?"
        if bt_text:
            self.button = tkinter.Button(parent, text = bt_text, command = self._function, width = 5)
            self.button.grid() #TODO : options
            text_bulle = description or label or bt_text or ""
            if key:
                text_bulle += "(Racc. : %s)"%key[0]
            self.infobulle = InfoBulle(parent=self.button,texte=text_bulle)

    def _function(self):
        '''The function called by the ui
            get nb_args in the stack
            put the result(s) in the stack
        '''
        logging.debug("Function %s called by %s"%(self.name, self))
        has_command_line = self.fcalc.command_line()
        if has_command_line:
            try:
                self.fcalc.stack.put_values(float(self.fcalc.command_line()))
                self.fcalc.v_command_line.set("")
            except ValueError as e:
                logging.info(e)
        if (not self.is_return) or (not has_command_line):
            try:
                if self.nb_args == "All":
                    args = self.fcalc.stack.get_all()
                else:
                    args = self.fcalc.stack.get(self.nb_args)
                self.execute_function(*args)
            except Fcalc_error_stacktoosmall:
                logging.info("Not enought arguments.")
            except (ArithmeticError, ValueError) as e:
                logging.info(e)
                self.fcalc.stack.put(args)

    def execute_function(self, *args):
        '''Execut the fonction and put result and self to stack
        '''
        values = self.function(*[item.get() for item in args])
        if type(values)!=tuple:
            values = [values]
        for value in values:
            self.fcalc.stack.put_items(StackItem(self.fcalc.stack, value, self, args))

class Function_stack(Function):
    '''Function for stack manipulation
    '''
    def execute_function(self, *args):
        '''Execut the stack manipulation function
        '''
        items = self.function(*args)
        if type(items)!=tuple:
            items = [items]
        if len(items)>0:
            for item in items:
                self.fcalc.stack.put_items(item)
        else:
            #Dans le cas où rien n'est retourné (ie suppression), on va remplit une stack fictiv
            item = StackItem(self.fcalc.stack, None, self, args)
            self.fcalc.stack.put_fictive_items(item)

class Function_angle_out(Function):
    '''Function qui renvoie un angle (soit deg, soit rad)
    '''
    def execute_function(self, *args):
        '''Execut the fonction and put result and self to stack
        '''
        values = self.function(*[item.get() for item in args])
        if type(values)!=tuple:
            values = [values]
        for value in values:
            if self.fcalc.options.get('deg_rad')=='rad':
                self.fcalc.stack.put_items(StackItem(self.fcalc.stack, value, self, args))
            else:
                self.fcalc.stack.put_items(StackItem(self.fcalc.stack, math.degrees(value), self, args))

class Function_angle_in(Function):
    '''Function qui prend des angles (soit deg, soit rad)
    '''
    def execute_function(self, *args):
        '''Execut the fonction and put result and self to stack
        '''
        if self.fcalc.options.get('deg_rad')=='rad':
            values = self.function(*[item.get() for item in args])
        else:
            values = self.function(*[math.radians(item.get()) for item in args])
        if type(values)!=tuple:
            values = [values]
        for value in values:
                self.fcalc.stack.put_items(StackItem(self.fcalc.stack, value, self, args))
