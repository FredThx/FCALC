# coding: utf8

'''
Un Frame tkinter
    qui représente le résumé de la stack (somme, moyenne, ...)
Usage :
'''
import tkinter as tkinter

from FUTIL.my_logging import *

class Summary(tkinter.Frame):
    '''A summary for the calculator
    '''

    functions = { \
            'Somme' : lambda *x : sum(x), \
            'Moyenne' : lambda *x : sum(x)/len(x), \
            'Nombre' : lambda *x : len(x)}

    def __init__(self, fcalc, *args, **kw):
        '''Initialisation

        '''
        self.fcalc = fcalc
        tkinter.Frame.__init__(self, fcalc.window, relief = 'groove',borderwidth = 2, *args, **kw)
        self.v_type = tkinter.StringVar()
        self.value = tkinter.DoubleVar()
        self.value.set(0)
        self.v_type.set(list(Summary.functions.keys())[0])
        for f in Summary.functions:
            tkinter.Radiobutton(self, variable = self.v_type, text = f, value = f, command = self.update).grid( sticky = 'nw')
        tkinter.Label(self, textvariable  = self.value).grid()

    def update(self):
        '''Update the value
        '''
        self.value.set(Summary.functions[self.v_type.get()](*(self.fcalc.stack.get_values())))
