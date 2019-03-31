# coding: utf8

'''
Un Label tkinter
    qui représente un item de la stack
Usage :
'''
import tkinter as tkinter
from FUTIL.my_logging import *

class StackItem(tkinter.Label):
    '''Un item de la stack
    '''
    def __init__(self, stack, value = 0, calcul = None, *args, **kw):
        '''Initialisation
            value : the value
            calcul : todo
        '''
        self.v_value = tkinter.DoubleVar()
        self.v_value.set(value)
        self.calcul = calcul
        self.stack = stack
        tkinter.Label.__init__(self, stack.interior, textvariable = self.v_value, width = 15, anchor = 'sw',justify = 'right')
        self.bind('<Button-1>', self.is_clicked1)
        self.bind('<Button-3>', self.is_clicked3)


    def get(self):
        '''Return the value
        '''
        return self.v_value.get()

    def set(self, value):
        '''Set the value
        '''
        self.v_value.set(value)

    def is_clicked1(self, event):
        '''event when cliked left
        '''
        logging.debug("%s is left-clicked : %s"%(self, event))
        self.stack.put(self.get())

    def is_clicked3(self, event):
        '''event when cliked right
        '''
        logging.debug("%s is right-clicked : %s"%(self, event))
        self.stack.items.remove(self)
        self.destroy()
