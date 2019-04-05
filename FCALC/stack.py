# coding: utf8

'''
Un Frame tkinter
    qui représente la stack de la calc
Usage :
'''
import tkinter as tkinter

from .scrframe import *
from .stack_item import *
from .fcalc_error import *
from FUTIL.my_logging import *

class Stack(VerticalScrolledFrame):
    '''A stack for the calculator
    '''
    def __init__(self, fcalc, height = None, *args, **kw):
        '''Initialisation
            width		:	nb de colonnes (y compris l'index)
            col_names	:	tableau des noms de colonnes
        '''
        self.fcalc = fcalc
        VerticalScrolledFrame.__init__(self, fcalc.window, height = height, relief = 'groove',borderwidth = 5, *args, **kw)
        self.items = []
        item = StackItem(self,0)
        item.grid()
        self.items.append(item)#TODO : remove

    def get(self, nb_args=1):
        '''Take nb_args value in the stack
            return a tuple
        '''
        if len(self.items)<nb_args:
            raise Fcalc_error_stacktoosmall(nb_args, len(self.items))
        args = []
        for i in range(nb_args):
            item = self.items.pop()
            logging.debug("take %s from stack"%item.get())
            args.append(item.get())
            item.destroy()
        args.reverse()
        self.is_updated()
        return tuple(args)

    def get_all(self):
        ''' Return all the stack and remove them
        '''
        return self.get(len(self.items))

    def put(self, values):
        ''' Put value or (value1, value2, ...) in the stack
        '''
        if type(values)!=tuple:
            values = [values]
        for value in values:
            item = StackItem(self,value)
            self.items.append(item)
            item.grid()
            logging.debug("Put %s to stack"%value)
        self.is_updated()

    def get_values(self):
        '''Return a list of values in the stack
        '''
        return [item.get() for item in self.items]

    def is_updated(self):
        '''Execute when the stack updated
        '''
        self.fcalc.summary.update()
