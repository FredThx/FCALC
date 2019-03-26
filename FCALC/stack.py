# coding: utf8

'''
Un Frame tkinter
    qui représente la stack de la calc
Usage :
'''
import tkinter as tkinter

from .scrframe import *
from.stack_item import *

class Stack(VerticalScrolledFrame):
    '''A stack for the calculator
    '''
    def __init__(self, parent, height = None, *args, **kw):
        '''Initialisation
            width		:	nb de colonnes (y compris l'index)
            col_names	:	tableau des noms de colonnes
        '''
        VerticalScrolledFrame.__init__(self, parent, height = height, relief = 'groove',borderwidth = 5, *args, **kw)
        self.items = []
        self.items.append(StackItem(self.interior,42.0).grid())
