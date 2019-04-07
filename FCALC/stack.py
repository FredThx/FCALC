# coding: utf8

'''
Un Frame tkinter
    qui représente la stack de la calc
Usage :
'''
import tkinter as tkinter
import logging

from .scrframe import *
from .stack_item import *
from .fcalc_error import *


class Stack(VerticalScrolledFrame):
    '''A stack for the calculator
    '''
    def __init__(self, fcalc, height = None, **kw):
        '''Initialisation
            width		:	nb de colonnes (y compris l'index)
            col_names	:	tableau des noms de colonnes
        '''
        self.fcalc = fcalc
        VerticalScrolledFrame.__init__(self, fcalc.window, height = height, relief = 'groove',borderwidth = 5, **kw)
        self.items = []
        item = StackItem(self,0)
        item.grid()
        self.items.append(item)#TODO : remove

    def grid(self, **kwargs):
        options = { \
                    'padx' : 5, 'pady' : 5
                    }
        options.update(kwargs)
        super().grid(**options)

    def get(self, nb_args=1):
        '''Take nb_args value in the stack
            return a tuple of StackItem
        '''
        if len(self.items)<nb_args:
            raise Fcalc_error_stacktoosmall(nb_args, len(self.items))
        args = []
        for i in range(nb_args):
            item = self.items.pop()
            logging.debug("take %s from stack"%str(item))
            args.append(item.clone())
            item.destroy()#TODO : verif destroy 100%
        args.reverse()
        self.is_updated()
        return tuple(args)

    def get_all(self):
        ''' Return all the stack and remove them
        '''
        return self.get(len(self.items))

    def put_values(self, values):
        ''' Put value or (value1, value2, ...) in the stack
            - values            :   value or (value1, value2, ...)
        '''
        if type(values)!=tuple:
            values = [values]
        for value in values:
            item = StackItem(self, value)
            self.items.append(item)
            item.grid()
            logging.debug("Put %s to stack"%str(item))
        self.is_updated()

    def put_items(self, *items):
        ''' Put items in the stack
        '''
        if type(items)!=tuple:
            logging.debug('oups')
            items = [items]
        for item in items:
            logging.debug("Put %s to stack"%str(item))
            self.items.append(item)
            item.grid()
        self.is_updated()

    def get_values(self, nb = None):
        '''Return a list of values in the stack
            nb  :   nb de valeur (default : None => All)
        '''
        if nb==None:
            return [item.get() for item in self.items]
        else:
            if len(self.items)<nb:
                raise Fcalc_error_stacktoosmall(nb, len(self.items))
            else:
                return [item.get() for item in self.items][-nb:]

    def is_updated(self):
        '''Execute when the stack updated
        '''
        self.fcalc.summary.update()
