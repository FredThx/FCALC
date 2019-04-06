# coding: utf8

import tkinter as tkinter
from FCALC.stack import *
from FCALC.function import *
from FUTIL.my_logging import *
from .stack_item import *
from .summary import *
from .options import *
import math
import clipboard
from .autogrid import *

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
        # La zone des options
        self.options= Options(self)
        self.options.grid(column = 2, row = 0)
        #Une zone avec des boutons
        self.buttons = tkinter.Frame(self.window, width = 100)
        self.buttons.grid(column = 0, row = 0, rowspan =2)
        #self.buttons.grid_propagate(0)
        # Une zone avec la pile
        self.stack = Stack(self,300)
        self.stack.grid(column = 1, row = 0, rowspan = 1)
        # Deg - Rad
        #TODO

        # La ligne de commandes
        self.v_command_line = tkinter.StringVar()
        self.t_command_line = tkinter.Entry(self.window, textvariable = self.v_command_line)
        self.t_command_line.grid(column = 1, row = 2)
        self.t_command_line.focus_set()
        # La zone des sommes
        self.summary = Summary(self)
        self.summary.grid(column = 2, row = 1)
        # key manager
        self.window.bind_all("<Key>", self.key_manager)
        # CTRL-C for copy
        self.window.bind_all("<Control-c>", self.ctrlc)

        # Les fonction

        # fonction de manipulation de stack (pas d'historisation)
        #self.bt_stack = AutoGrid(self.buttons)
        self.bt_stack = Frame(self.buttons)
        self.bt_stack.grid(row = 0)
        Function_stack(self, self.bt_stack, lambda x : (x,x.clone()) , nb_args = 1 ,bt_text = "Dup", key = ["Return","KP_Enter"], is_return = True, delete1car = False)
        Function_stack(self, self.bt_stack, lambda x : () , nb_args = 1 ,bt_text = "CE", key = "Delete", delete1car = False)
        Function_stack(self, self.bt_stack, lambda x, y : (y,x)  , nb_args = 2 ,bt_text = "SWAP", key = ["s","S"])
        Function_stack(self, self.bt_stack, lambda *x : ()  , nb_args = "All" ,bt_text = "CLEAR")
        Function_stack(self, self.bt_stack, lambda *x : x[1:]+(x[0],)  , nb_args = "All" ,bt_text = "ROLL", key = ["r", "R"])
        Function_stack(self, self.bt_stack, lambda x : x.undo() , nb_args = 1 ,bt_text = "Undo", key = ["u","U"])
        #Opérations basiques
        #self.bt_basic = AutoGrid(self.buttons)
        self.bt_basic = Frame(self.buttons)
        self.bt_basic.grid(row = 2)
        Function(self, self.bt_basic, lambda x,y : x+y , nb_args = 2 ,bt_text = "+", key = ["plus","KP_Add"])
        Function(self, self.bt_basic, lambda x,y : x-y  , nb_args = 2 ,bt_text = "-", key = ["minus","KP_Subtract"])
        Function(self, self.bt_basic, lambda x,y : x*y  , nb_args = 2 ,bt_text = "*", key = ["asterisk","KP_Multiply"])
        Function(self, self.bt_basic, lambda x,y : x/y  , nb_args = 2 ,bt_text = "/", key = ["slash","KP_Divide"])
        Function(self, self.bt_basic, lambda x : 1/x  , nb_args = 1 ,bt_text = "1/x", key = ["i","I"])
        #Fonction Trigo #TODO : gestion DEG-RAD
        #self.bt_trig = AutoGrid(self.buttons)
        self.bt_trig = Frame(self.buttons)
        self.bt_trig.grid(row = 1)
        Function_angle_out(self, self.bt_trig, lambda *x : math.pi , nb_args = 0 ,bt_text = "PI")
        Function_angle_in(self, self.bt_trig, lambda x : math.sin(x) , nb_args = 1 ,bt_text = "SIN")
        Function_angle_in(self, self.bt_trig, lambda x : math.cos(x) , nb_args = 1 ,bt_text = "COS")
        Function_angle_out(self, self.bt_trig, lambda x : math.asin(x) , nb_args = 1 ,bt_text = "ASIN")
        Function_angle_out(self, self.bt_trig, lambda x : math.acos(x) , nb_args = 1 ,bt_text = "ACOS")
        Function_angle_in(self, self.bt_trig, lambda x : math.tan(x) , nb_args = 1 ,bt_text = "TAN")
        Function_angle_out(self, self.bt_trig, lambda x : math.atan(x) , nb_args = 1 ,bt_text = "ATAN")
        Function_angle_out(self, self.bt_trig, lambda x : math.atan2(x) , nb_args = 2 ,bt_text = "ATAN2")



    def key_manager(self, event):
        ''' MAnage the key events
        '''
        logging.debug("Key pressed : '%s'"%event.keysym)
        if event.keysym in self.keys:
            f = self.keys[event.keysym]
            if f.delete1car:
                self.v_command_line.set(self.command_line()[0:-1])
            f._function()

    def ctrlc(self, event):
        '''Intercept CRTL-C for copy to clipboard
        '''
        logging.debug("CRTL-C")
        if len(self.v_command_line.get())==0:
            clipboard.copy(str(self.stack.get_values(1)[0]))
        else:
            clipboard.copy(self.v_command_line.get())


    def command_line(self):
        '''Return the command line or None
        '''
        if len(self.v_command_line.get())==0:
            return None
        else:
            return self.v_command_line.get()
