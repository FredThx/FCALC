# coding: utf8

import tkinter as tkinter
from FCALC.stack import *

class Fcalc(object):
    '''Application Calculatrice
    '''
    def __init__(self, title = "Calculatrice"):
        self.window = tkinter.Tk()
        self.title = title
        self.init_ui()

    def run(self):
        self.window.mainloop()

    def init_ui(self):
        '''Init the ui
        '''
        self.window.title(self.title)
        #Une zone avec des boutons
        self.ui_buttons = tkinter.Frame(self.window)
        self.ui_buttons.grid(column = 0, rowspan =2)
        # Une zone avec la pile
        self.ui_stack = Stack(self.window,300)
        self.ui_stack.grid(column = 1, row = 0)
        # La ligne de commandes
        self.ui_command_line = tkinter.Entry(self.window)
        self.ui_command_line.grid(column = 1, row = 1)
