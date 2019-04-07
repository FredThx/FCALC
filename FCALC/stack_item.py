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
    def __init__(self, stack, value = 0, function = None, args = ()):
        '''Initialisation
            - value             : the value
            - function          : function off the calcul (optional)
            - args              : args of the function (StackItem)
        '''
        self.v_text = tkinter.StringVar()
        self.value = value
        self.function = function
        self.args = args
        self.stack = stack
        self.v_text.set(str(self))
        tkinter.Label.__init__(self, stack.interior, textvariable = self.v_text, width = 30, anchor = 'sw',justify = 'right')
        self.bind('<Button-1>', self.is_clicked1)
        self.bind('<Button-3>', self.is_clicked3)


    def get(self):
        '''Return the value
        '''
        return self.value

    def __str__(self): #TODO : faire plus lisible!
        if self.stack.fcalc.options.get('detail')=='on' and self.function:
            return "%s=%s(%s)"%(self.value, self.function.name, [str(arg) for arg in self.args])
        else:
            return str(self.value)

    __repr__ = __str__ # A LA CON, mais ça marche

    def set(self, value):
        '''Set the value
        '''
        logging.debug("Modif uniquement value, pas function!!")
        self.value = value

    def is_clicked1(self, event):
        '''event when cliked left
        '''
        logging.debug("%s is left-clicked : %s"%(self, event))
        self.stack.put_items(self.clone())

    def is_clicked3(self, event):
        '''event when cliked right
        '''
        logging.debug("%s is right-clicked : %s"%(self, event))
        self.stack.items.remove(self)
        self.destroy()

    def clone(self):
        new_item = StackItem(self.stack, self.value, self.function, self.args)
        return new_item

    def update(self):
        '''Update the label
        '''
        self.v_text.set(str(self))

    def undo(self):
        ''' Return the args of the function
        '''
        return self.args
