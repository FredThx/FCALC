# coding: utf8

'''
Un Frame tkinter
    qui represente une barre de boutons
'''
import tkinter
import logging

class Buttonframe(tkinter.LabelFrame):
    '''Cadre de buttons autogrid
    '''
    def __init__(self, master = None, **kwargs):
        tkinter.LabelFrame.__init__(self, master, **kwargs)
        self.columns = 0
        self.bind('<Configure>', self.regrid)

    def grid(self, **kwargs):
        options = {'sticky' : tkinter.E + tkinter.W, \
                    'padx' : 5, 'pady' : 5
                    }
        options.update(kwargs)
        super().grid(**options)

    def regrid(self, event=None):
        width = self.winfo_width()
        slaves = self.grid_slaves()
        max_width = max(slave.winfo_width() for slave in slaves)
        cols = width // max_width
        if cols == self.columns: # if the column number has not changed, abort
            return
        for i, slave in enumerate(slaves):
            slave.grid_forget()
            slave.grid(row=i//cols, column=i%cols)
        self.columns = cols
