# coding: utf8

'''
Un Label tkinter
    qui représente un item de la stack
Usage :
'''
import tkinter as tkinter

class StackItem(tkinter.Label):
    '''Un item de la stack
    '''
    def __init__(self, parent, value = 0, calcul = None, *args, **kw):
        '''Initialisation
            value : the value
            calcul : todo
        '''
        self.v_value = tkinter.DoubleVar()
        self.v_value.set(value)
        self.calcul = calcul
        tkinter.Label.__init__(self, parent, textvariable = self.v_value, width = 15, anchor = 'sw',justify = 'right')
