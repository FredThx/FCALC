# coding: utf8

'''
Un Frame tkinter
    qui représente les option de la calculatrice (deg_rad, ...)
Usage :
'''
import tkinter as tkinter

from FUTIL.my_logging import *

class Options(tkinter.Frame):
    '''Options for the calculator
    '''

    options = { \
            'deg_rad' : ['rad', 'deg'], \
            'detail' : ['off', 'on']
            }

    def __init__(self, fcalc, parent, *args, **kw):
        '''Initialisation
        '''
        self.fcalc = fcalc
        tkinter.Frame.__init__(self, parent, relief = 'groove',borderwidth = 2, *args, **kw)
        self.opts = {}
        for option in Options.options:
            self.opts[option] = tkinter.StringVar()
            self.opts[option].set(Options.options[option][0])
            frame = tkinter.LabelFrame(self,text = option)
            for choice in Options.options[option]:
                tkinter.Radiobutton(frame, variable = self.opts[option], text = choice, value = choice, command = self.update).grid( sticky = 'nw')
            frame.grid()

    def grid(self, **kwargs):
        options = {'sticky' : tkinter.E + tkinter.W, \
                    'padx' : 5, 'pady' : 5
                    }
        options.update(kwargs)
        super().grid(**options)

    def update(self):
        '''Update the value
        '''
        for item in self.fcalc.stack.items:
            item.update()

    def get(self, option):
        '''Return the value of the option
        '''
        return self.opts[option].get()
