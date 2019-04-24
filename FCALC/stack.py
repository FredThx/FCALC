# coding: utf8

'''
Un Frame tkinter
    qui représente la stack de la calc
Usage :
'''
import tkinter as tkinter
import logging
import locale
import csv

from .scrframe import *
from .stack_item import *
from .fcalc_error import *
from . import clipboard


class Stack(VerticalScrolledFrame):
    '''A stack for the calculator
    '''
    def __init__(self, fcalc, parent, height = None, **kw):
        '''Initialisation
            width		:	nb de colonnes (y compris l'index)
            col_names	:	tableau des noms de colonnes
        '''
        self.fcalc = fcalc
        VerticalScrolledFrame.__init__(self, parent, height = height, min_width = 200, relief = 'groove',borderwidth = 5, **kw)
        self.items = []
        self.fictive_items = []
        self.bt_trash = tkinter.Button(self, text = "UNDELETE", command = self.undelete, state = 'disabled',wraplength = 1 )
        self.bt_trash.pack()#side = tkinter.LEFT)
        #Menu contextuele
        self.aMenu = tkinter.Menu(self, tearoff = 0)
        self.aMenu.add_command(label = 'Vider', command = lambda:self.del_items('ALL'))
        self.aMenu.add_command(label = 'Vider historique', command = self.clean_fictive_items)
        self.aMenu.add_command(label = 'Copier tout', command = self.fcalc.copy_all)
        self.bind('<Button-3>', self.popup_menu)


    def grid(self, **kwargs):
        options = { \
                    'padx' : 5, 'pady' : 5, 'sticky' : 'nesw'
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

    def del_items(self, *items):
        '''remove items from stack
        and copy tem in the fictive_items list
        *item        :   item object
        if the first item = 'ALL' ...
        '''
        if len(items)>0 and items[0] == 'ALL':
            items = self.items.copy()
        for item in items:
            self.items.remove(item)
            item.grid_forget()
            self.put_fictive_items(item)
        self.is_updated()


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
            logging.debug("Put new %s to stack"%str(item))
        self.is_updated()

    def put_items(self, *items):
        ''' Put items in the stack
        '''
        if type(items)!=tuple:
            logging.debug('oups')
            items = [items]
        for item in items:
            logging.debug("Put existing %s to stack"%str(item))
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
        try:
            self.fcalc.summary.update()
        except:
            pass

    def put_fictive_items(self, *items):
        '''Put the item in a fictive stack (non visible, juste for undelete)
        '''
        if type(items)!=tuple:
            items = [items]
        for item in items:
            self.fictive_items.append(item)
        self.bt_trash.config(state='normal')

    def get_fictive_item(self):
        ''' Get a item in the fictive stack and remove it from the fictive_items list
        '''
        return self.fictive_items.pop()

    def undelete(self):
        ''' Move the last item from the fictive_items list to the stack and undo it.
        '''
        item = self.get_fictive_item()
        self.put_items(*item.undo())
        if len(self.fictive_items)==0:
            self.bt_trash.config(state='disabled')

    def clean_fictive_items(self):
        '''remove all fictives_items
        '''
        while len(self.fictive_items)>0:
            item = self.fictive_items.pop()
            item.destroy()
        self.bt_trash.config(state='disabled')

    def move(self, item, position):
        '''Move a item to position in the items list
        '''
        actual_position = self.items.index(item)
        self.items.insert(position, self.items.pop(actual_position))

    def popup_menu(self, event):
        '''Show the context menu
        '''
        self.aMenu.post(event.x_root, event.y_root)

    def copy_to_clipboard(self, item = None):
        '''Copy the value of the item to clipboard
        if item is None, the last one is used
        '''
        if not item:
            item = self.get_values(1)[0]
        clipboard.copy(locale.str(item.get()))

    def set_font(self):
        '''Change the font of all items
        '''
        for item in self.items:
            item.set_font()
        for item in self.fictive_items:
            item.set_font()
    def export_csv(self, file):
        '''Export the values to a cvs file
        If fail, return the exception
        else return True
        '''
        try:
            with open(file, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';')
                for item in self.items:
                    spamwriter.writerow([locale.str(item.get())])
            return True
        except Exception as e:
            return e
