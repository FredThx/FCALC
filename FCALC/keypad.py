# coding: utf8

import tkinter as tkinter


class Keypad(tkinter.Frame):
    '''Un pavé numérique
    '''
    def __init__(self, parent, callback, *args, **kw):
        '''Initialisation
            parent      :   The tkinter parent
            callback    :    Fonction called when key pressed
        '''
        self.callback = callback
        tkinter.Frame.__init__(self, parent, relief = 'groove',borderwidth = 2, *args, **kw)
        tkinter.Button(self, text = "CE", command = lambda: self.do_event('Delete'), width = 3, height = 2).grid(row=0, column = 0)
        tkinter.Button(self, text = "/", command = lambda: self.do_event('slash'), width = 3, height = 2).grid(row=0, column = 1)
        tkinter.Button(self, text = "*", command = lambda: self.do_event('asterisk'), width = 3, height = 2).grid(row=0, column = 2)
        tkinter.Button(self, text = "-", command = lambda: self.do_event('minus'), width = 3, height = 2).grid(row=0, column = 3)
        tkinter.Button(self, text = "+", command = lambda: self.do_event('plus'), width = 3, height = 5).grid(row=1, column = 3, rowspan = 2)
        tkinter.Button(self, text = "Entr", command = lambda: self.do_event('Return'), width = 3, height = 5).grid(row=3 , column = 3, rowspan = 2)
        tkinter.Button(self, text = "1", command = lambda: self.do_event('1'), width = 3, height = 2).grid(row=3, column = 0)
        tkinter.Button(self, text = "2", command = lambda: self.do_event('2'), width = 3, height = 2).grid(row=3, column = 1)
        tkinter.Button(self, text = "3", command = lambda: self.do_event('3'), width = 3, height = 2).grid(row=3, column = 2)
        tkinter.Button(self, text = "4", command = lambda: self.do_event('4'), width = 3, height = 2).grid(row=2, column = 0)
        tkinter.Button(self, text = "5", command = lambda: self.do_event('5'), width = 3, height = 2).grid(row=2, column = 1)
        tkinter.Button(self, text = "6", command = lambda: self.do_event('6'), width = 3, height = 2).grid(row=2, column = 2)
        tkinter.Button(self, text = "7", command = lambda: self.do_event('7'), width = 3, height = 2).grid(row=1, column = 0)
        tkinter.Button(self, text = "8", command = lambda: self.do_event('8'), width = 3, height = 2).grid(row=1, column = 1)
        tkinter.Button(self, text = "9", command = lambda: self.do_event('9'), width = 3, height = 2).grid(row=1, column = 2)
        tkinter.Button(self, text = "0", command = lambda: self.do_event('0'), width = 6, height = 2).grid(row=4, column = 0, columnspan = 2)
        tkinter.Button(self, text = ".", command = lambda: self.do_event('period'), width = 3, height = 2).grid(row=4, column = 2)



    def do_event(self, txt):
        '''Execute the callback function with txt as argument
        '''
        self.callback(txt)
