# coding: utf8

import tkinter as tkinter
import tkinter.messagebox
import logging
import math
import locale

from .stack import *
from .function import *
from .stack_item import *
from .summary import *
from .options import *
from . import clipboard
from .buttons_frame import *
from .version import __version__

locale.setlocale(locale.LC_ALL, '')

class Fcalc(object):
    '''Application Calculatrice
    '''
    def __init__(self, title = "Calculatrice"):
        self.window = tkinter.Tk()
        self.title = title
        self.keys = {}
        self.init_ui()

    def run(self):
        self.window.mainloop()

    def init_ui(self):
        '''Init the ui
        '''
        self.window.title(self.title)

        #Une zone avec des boutons
        self.buttons = tkinter.Frame(self.window)
        self.buttons.columnconfigure(0,weight=1)
        # Une zone avec options et Summary
        self.zone3 = tkinter.Frame(self.window)
        self.zone3.columnconfigure(0,weight=1)
        # La zone des options
        self.options= Options(self, self.zone3)
        self.options.grid(column = 0, row = 0)
        # La zone des summary
        self.summary = Summary(self, self.zone3)
        self.summary.grid(column = 0, row = 1)
        # Une zone avec la pile
        self.stack = Stack(self,300)
        self.stack.grid(column = 1, row = 0, rowspan = 1)
        # La ligne de commandes
        self.v_command_line = tkinter.StringVar()
        self.t_command_line = tkinter.Entry(self.window, textvariable = self.v_command_line)
        self.t_command_line.grid(column = 1, row = 2, sticky = tkinter.S + tkinter.E + tkinter.W, padx = 10, pady = 5)
        self.t_command_line.focus_set()

        # key manager
        self.window.bind_all("<Key>", self.key_manager)
        # CTRL-C for copy
        self.window.bind_all("<Control-c>", lambda event : self.copy())
        # CTRL-V for Paste
        self.window.bind_all("<Control-v>", lambda event : self.paste())
        # CTRL-X for Paste
        self.window.bind_all("<Control-x>", lambda event : self.cut())
        # Les fonction
        # fonction de manipulation de stack (pas d'historisation)
        self.bts_stack = Buttonframe(self.buttons, text = "Stack")
        self.bts_stack.grid(row = 0)
        Function_stack(self, self.bts_stack, lambda x : (x,x.clone()) , nb_args = 1 ,bt_text = "Dup", key = ["Return","KP_Enter"], is_return = True, delete1car = False)
        Function_stack(self, self.bts_stack, lambda x : () , nb_args = 1 ,bt_text = "CE", key = "Delete", delete1car = False)
        Function_stack(self, self.bts_stack, lambda x, y : (y,x)  , nb_args = 2 ,bt_text = "SWAP", key = ["s","S"])
        Function_stack(self, self.bts_stack, lambda *x : ()  , nb_args = "All" ,bt_text = "CLEAR")
        Function_stack(self, self.bts_stack, lambda *x : x[1:]+(x[0],)  , nb_args = "All" ,bt_text = "ROLL", key = ["r", "R"])
        Function_stack(self, self.bts_stack, lambda x : x.undo() , nb_args = 1 ,bt_text = "Undo", key = ["u","U"])
        #Opérations basiques
        self.bts_basic = Buttonframe(self.buttons, text = "Basics")
        self.bts_basic.grid(row = 2)
        Function(self, self.bts_basic, lambda x,y : x+y , nb_args = 2 ,bt_text = "+", key = ["plus","KP_Add"])
        Function(self, self.bts_basic, lambda x,y : x-y  , nb_args = 2 ,bt_text = "-", key = ["minus","KP_Subtract"])
        Function(self, self.bts_basic, lambda x,y : x*y  , nb_args = 2 ,bt_text = "*", key = ["asterisk","KP_Multiply"])
        Function(self, self.bts_basic, lambda x,y : x/y  , nb_args = 2 ,bt_text = "/", key = ["slash","KP_Divide"])
        Function(self, self.bts_basic, lambda x : 1/x  , nb_args = 1 ,bt_text = "1/x", key = ["i","I"])
        #Fonction Trigo #TODO : gestion DEG-RAD
        self.bts_trig = Buttonframe(self.buttons, text = "Trigo")
        self.bts_trig.grid(row = 1)
        Function_angle_out(self, self.bts_trig, lambda *x : math.pi , nb_args = 0 ,bt_text = "PI")
        Function_angle_in(self, self.bts_trig, lambda x : math.sin(x) , nb_args = 1 ,bt_text = "SIN")
        Function_angle_in(self, self.bts_trig, lambda x : math.cos(x) , nb_args = 1 ,bt_text = "COS")
        Function_angle_out(self, self.bts_trig, lambda x : math.asin(x) , nb_args = 1 ,bt_text = "ASIN")
        Function_angle_out(self, self.bts_trig, lambda x : math.acos(x) , nb_args = 1 ,bt_text = "ACOS")
        Function_angle_in(self, self.bts_trig, lambda x : math.tan(x) , nb_args = 1 ,bt_text = "TAN")
        Function_angle_out(self, self.bts_trig, lambda x : math.atan(x) , nb_args = 1 ,bt_text = "ATAN")
        Function_angle_out(self, self.bts_trig, lambda x : math.atan2(x) , nb_args = 2 ,bt_text = "ATAN2")

        # Les menus
        self.menu_barre = tkinter.Menu(self.window,tearoff = 0)
        #Fichier
        self.menu_fichier = tkinter.Menu(self.menu_barre, tearoff =0 )
        self.menu_barre.add_cascade(label = 'Fichier', underline = 0, menu = self.menu_fichier)
        self.menu_fichier.add_command(label = 'Export stack', underline = 0, state=tkinter.DISABLED, command = self.export)
        self.menu_fichier.add_command(label = 'Quitter', underline = 0, command = self.window.quit)
        #Edition
        self.menu_edition = tkinter.Menu(self.menu_barre, tearoff =0)
        self.menu_barre.add_cascade(label = 'Edition', underline = 0, menu = self.menu_edition)
        self.menu_edition.add_command(label = 'Copier (CTRL-C)', underline = 13, command = self.copy)
        self.menu_edition.add_command(label = 'Copier Tout', underline = 7, command = self.copy_all)
        self.menu_edition.add_command(label = 'Couper (CTRL-X)', underline = 13, command = self.cut)
        self.menu_edition.add_command(label = 'Coller (CTRL-V)', underline = 13, command = self.paste)
        #Affichage
        self.menu_affichage = tkinter.Menu(self.menu_barre, tearoff =0)
        self.menu_barre.add_cascade(label = 'Affichage', underline = 0, menu = self.menu_affichage)
        self.v_buttons_visible = tkinter.IntVar()
        self.v_buttons_visible.set(1)
        self.menu_affichage.add_checkbutton(label = 'Boutons', underline = 0, variable = self.v_buttons_visible, command = self.toggle_buttons_visible)
        self.v_zone3_visible = tkinter.IntVar()
        self.v_zone3_visible.set(1)
        self.menu_affichage.add_checkbutton(label = 'Options-Résumé', underline = 0, variable = self.v_zone3_visible, command = self.toggle_zone3_visible)
        #Aide
        self.menu_aide = tkinter.Menu(self.menu_barre, tearoff =0)
        self.menu_barre.add_cascade(label = 'Aide', underline = 2, menu = self.menu_aide)
        self.menu_aide.add_command(label = 'A propos', underline = 0, command = self.about)
        self.window.config(menu = self.menu_barre)


        self.grid_buttons()
        self.grid_zone3()
        self.window.columnconfigure(1, minsize = 200, weight = 2)


    def grid_buttons(self):
        if self.v_buttons_visible.get():
            self.buttons.grid(column = 0, row = 0, rowspan =2, sticky = tkinter.N + tkinter.E + tkinter.W)
            self.window.columnconfigure(0, minsize = 120, weight = 1)
        else:
            self.buttons.grid_forget()
            self.window.columnconfigure(0, minsize = 0, weight = 1)

    def grid_zone3(self):
        if self.v_zone3_visible.get():
            self.zone3.grid(column = 2, row = 0, rowspan =2, sticky = tkinter.N + tkinter.E + tkinter.W)
            self.window.columnconfigure(2, minsize = 100, weight = 1)
        else:
            self.zone3.grid_forget()
            self.window.columnconfigure(2, minsize = 0, weight = 1)

    def key_manager(self, event):
        ''' MAnage the key events
        '''
        logging.debug("Key pressed : '%s'"%event.keysym)
        if event.keysym in self.keys:
            f = self.keys[event.keysym]
            if f.delete1car:
                self.v_command_line.set(self.command_line()[0:-1])
            f._function()

    def ctrlz(self, event):
        pass

    def command_line(self):
        '''Return the command line or None
        '''
        if len(self.v_command_line.get())==0:
            return None
        else:
            return self.v_command_line.get()

    def about(self):
        tkinter.messagebox.showinfo("A propos de la calculatrice", \
            "Une calculatrice RPN (Polonaise inverse)\n \
            Auteur : FredThx\n \
            Version : %s\n \
            https://github.com/FredThx/FCALC"%__version__
                    )
    def export(self):
        pass

    def copy(self):
        '''Copy command_line or last stack_item
        '''
        if len(self.v_command_line.get())==0:
            clipboard.copy(locale.str(self.stack.get_values(1)[0]))
        else:
            try:
                clipboard.copy(locale.str(float(self.v_command_line.get())))
            except:
                clipboard.copy(self.v_command_line.get())

    def copy_all(self):
        '''Copy all the values from the stack with '\n' betwween values
        '''
        clipboard.copy("\n".join([locale.str(i) for i in self.stack.get_values()]))

    def paste(self):
        '''Paste one or more data from the clipboard
        '''
        txt = clipboard.paste()
        #Windows : \r\n Linux-mac : \n
        txts = [t.replace('\r','') for t in txt.split('\n') if len(t)>0]
        for t in txts:
            try:
                val = locale.atof(t)
                self.stack.put_values(val)
            except ValueError:
                pass
        self.v_command_line.set("")

    def cut(self):
        '''Cut command_line or last stack_item
        '''
        self.copy()
        if len(self.v_command_line.get())>0:
            self.v_command_line.set("")
        else:
            self.stack.get()

    @staticmethod
    def toogle(v_val):
        if v_val.get():
            v_val.set(1)
        else:
            v_val.set(0)
    def toggle_buttons_visible(self):
        self.toogle(self.v_buttons_visible)
        self.grid_buttons()
    def toggle_zone3_visible(self):
        self.toogle(self.v_zone3_visible)
        self.grid_zone3()
