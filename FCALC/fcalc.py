# coding: utf8

import tkinter as tkinter
import tkinter.messagebox
import tkinter.filedialog
import logging
import math, statistics
import locale
import json
import os
import wget

import webbrowser

from . import clipboard
from .stack import *
from .function import *
from .stack_item import *
from .summary import *
from .options import *
from .buttons_frame import *
from .keypad import *
from .version import __version__
from .github import *
from .get_application_path import *

locale.setlocale(locale.LC_ALL, '')

class Fcalc(object):
    '''Application Calculatrice
    '''
    fonts = [8,10,12,14,16,18,24]

    github_owner = "FredThx"
    github_repo = "FCALC"

    def __init__(self, title = "Calculatrice", url_help = None, option_gui = None):
        self.window = tkinter.Tk()
        self.path = os.path.expanduser('~')
        self.title = title
        self.url_help = url_help
        self.keys = {}
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        if option_gui:
            try:
                self.window.option_readfile(option_gui)
            except:
                logging.warning(f"Error reading {option_gui}")
        self.init_ui()
        self.check_update()

    def run(self):
        self.window.mainloop()

    def init_ui(self):
        '''Init the ui
        '''
        self.window.title(self.title)

        #Une zone avec des boutons
        self.buttons = tkinter.Frame(self.window)
        self.buttons.columnconfigure(0,weight=1)
        ## Une zone avec options et Summary
        self.zone3 = tkinter.Frame(self.window)
        self.zone3.columnconfigure(0,weight=1)
        # La zone des options
        self.options= Options(self, self.zone3)
        self.options.grid(column = 0, row = 0)
        # La zone des summary
        self.summary = Summary(self, self.zone3)
        self.summary.grid(column = 0, row = 1)
        ## Une zone avec la stack, la ligne de commande et le Keypad
        self.zone2 = tkinter.Frame(self.window)
        self.zone2.grid(column = 1, row = 0, sticky = 'nesw')
        # Stack
        self.stack = Stack(self,self.zone2)
        self.stack.grid(column = 0, row = 0)
        # La ligne de commandes
        self.v_command_line = tkinter.StringVar()
        self.t_command_line = tkinter.Entry(self.zone2, textvariable = self.v_command_line)
        self.t_command_line.grid(column = 0, row = 1, sticky = tkinter.S + tkinter.E + tkinter.W, padx = 10, pady = 5)
        self.t_command_line.focus_set()
        # keypad
        self.keypad = Keypad(self.zone2, self.do_keypad_event)

        #PARAMETRES
        #Set default params
        self.v_auto_save_config = tkinter.IntVar()
        self.v_auto_save_config.set(1)
        self.v_auto_save_data = tkinter.IntVar()
        self.v_auto_save_data.set(0)
        self.v_buttons_visible = {}
        self.buttons_frame_name = ["stack", "basics", "trigo", "maths", "stats"]
        for button_frame in self.buttons_frame_name:
            self.v_buttons_visible[button_frame] = tkinter.IntVar()
            self.v_buttons_visible[button_frame].set(0)
        self.v_zone3_visible = tkinter.IntVar()
        self.v_zone3_visible.set(0)
        self.v_keypad_visible = tkinter.IntVar()
        self.v_keypad_visible.set(0)
        self.v_font = tkinter.IntVar()
        self.v_font.set(12)
        #Load a json file with last params
        self.load()

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
        self.bts = {}
        self.bts['stack'] = Buttonframe(self.buttons, text = "Stack")
        self.bts['stack'].grid(row = 0)
        Function_stack(self, self.bts['stack'], lambda x : (x,x.clone()) , nb_args = 1 ,bt_text = "Dup", key = ["Return","KP_Enter"], is_return = True, delete1car = False)
        Function_stack(self, self.bts['stack'], lambda x : () , nb_args = 1 ,bt_text = "CE", key = "Delete", delete1car = False)
        Function_stack(self, self.bts['stack'], lambda x, y : (y,x)  , nb_args = 2 ,bt_text = "SWAP", key = ["s","S"])
        Function_stack(self, self.bts['stack'], lambda *x : ()  , nb_args = "All" ,bt_text = "CLEAR")
        Function_stack(self, self.bts['stack'], lambda *x : x[1:]+(x[0],)  , nb_args = "All" ,bt_text = "ROLL", key = ["r", "R"])
        Function_stack(self, self.bts['stack'], lambda x : x.undo() , nb_args = 1 ,bt_text = "Undo", key = ["u","U"])
        #Opérations basiques
        self.bts['basics'] = Buttonframe(self.buttons, text = "Basics")
        self.bts['basics'].grid(row = 2)
        Function_operator(self, self.bts['basics'], lambda x,y : x+y , nb_args = 2 ,key = ["plus","KP_Add"], label = "+")
        Function_operator(self, self.bts['basics'], lambda x,y : x-y  , nb_args = 2 , key = ["minus","KP_Subtract"], label = "-")
        Function_operator(self, self.bts['basics'], lambda x,y : x*y  , nb_args = 2 , key = ["asterisk","KP_Multiply"], label = "*")
        Function_operator(self, self.bts['basics'], lambda x,y : x/y  , nb_args = 2 , key = ["slash","KP_Divide"], label = "/")
        Function(self, self.bts['basics'], lambda x : 1/x  , nb_args = 1 ,bt_text = "1/x", key = ["i","I"], format = "1/%s")
        Function(self, self.bts['basics'], lambda x : -x  , nb_args = 1 ,bt_text = "+/-", key = ["n","N"], format = "-%s")
        Function(self, self.bts['basics'], lambda x,y : (y-x)/x  , nb_args = 2 , bt_text = "Aug%", key = ["A","a"], description = "x,y : (y-x)/y", format = "Aug(%s,%s)")
        Function(self, self.bts['basics'], lambda x : x*x, nb_args = 1, bt_text = "x^2", description = "carré")
        Function(self, self.bts['basics'], lambda x,y : x**y, nb_args = 2, bt_text = "x^y", key = ["P","p"], description = "x puiss. y")
        Function(self, self.bts['basics'], lambda x : x**0.5, nb_args = 1, bt_text = "SQRT", key = ["R","r"], description = "Racinne")
        #Fonction Trigo #TODO : gestion DEG-RAD
        self.bts['trigo'] = Buttonframe(self.buttons, text = "Trigo")
        self.bts['trigo'].grid(row = 1)
        Function_angle_out(self, self.bts['trigo'], lambda *x : math.pi , nb_args = 0 ,bt_text = "PI")
        Function_angle_in(self, self.bts['trigo'], lambda x : math.sin(x) , nb_args = 1 ,bt_text = "SIN")
        Function_angle_in(self, self.bts['trigo'], lambda x : math.cos(x) , nb_args = 1 ,bt_text = "COS")
        Function_angle_out(self, self.bts['trigo'], lambda x : math.asin(x) , nb_args = 1 ,bt_text = "ASIN")
        Function_angle_out(self, self.bts['trigo'], lambda x : math.acos(x) , nb_args = 1 ,bt_text = "ACOS")
        Function_angle_in(self, self.bts['trigo'], lambda x : math.tan(x) , nb_args = 1 ,bt_text = "TAN")
        Function_angle_out(self, self.bts['trigo'], lambda x : math.atan(x) , nb_args = 1 ,bt_text = "ATAN")
        Function_angle_out(self, self.bts['trigo'], lambda x : math.atan2(x) , nb_args = 2 ,bt_text = "ATAN2")
        Function(self, self.bts['trigo'], lambda x : math.degrees(x) , nb_args = 1 ,bt_text = "->Deg")
        Function(self, self.bts['trigo'], lambda x : math.radians(x) , nb_args = 1 ,bt_text = "->Rad")

        #Mathématiques
        self.bts['maths'] = Buttonframe(self.buttons, text = "Maths")
        self.bts['maths'].grid(row = 3)
        Function(self, self.bts['maths'], lambda x : math.exp(x)  , nb_args = 1 , bt_text = "Exp", key = ["E","e"], description = "x : exp(x)", format = "e^%s")
        Function(self, self.bts['maths'], lambda x : math.log(x)  , nb_args = 1 , bt_text = "Ln", key = ["L","l"], description = "x : ln(x)", format = "ln(%s)")
        Function(self, self.bts['maths'], lambda x : math.log10(x)  , nb_args = 1 , bt_text = "Log10", key = [], description = "x : log10(x)", format = "log10(%s)")
        #Statistiques
        self.bts['stats'] = Buttonframe(self.buttons, text = "Statistiques")
        self.bts['stats'].grid(row = 4)
        Function_n_args(self, self.bts['stats'], lambda *x : statistics.mean(x) , bt_text = "x̄", label = "mean", key = ["M","m"], description = "a1,...an,n : Σ(a1,...an)/n")
        Function_n_args(self, self.bts['stats'], lambda *x : statistics.median(x) , bt_text = "Median", label = "Median", key = [], description = "a1,...an,n : Median(a1,...an)")
        Function_n_args(self, self.bts['stats'], lambda *x : statistics.stdev(x) , bt_text = "σ", label = "Ecartype", key = [], description = "a1,...an,n : √(variance(a1,...an))")
        def six_sigma(*x):
            moy = statistics.mean(x)
            ecartype = statistics.stdev(x)
            return (moy - 3*ecartype, moy + 3*ecartype)
        Function_n_args(self, self.bts['stats'], six_sigma , bt_text = "6σ", label = "6σ", key = [], description = "a1,...an,n : (x̄-3σ,x̄+3σ)")
        # Les menus
        self.menu_barre = tkinter.Menu(self.window,tearoff = 0)
        #Fichier
        self.menu_fichier = tkinter.Menu(self.menu_barre, tearoff =0 )
        self.menu_barre.add_cascade(label = 'Fichier', underline = 0, menu = self.menu_fichier)
        self.menu_fichier.add_command(label = 'Export stack', underline = 0, command = self.export)
        self.menu_fichier.add_checkbutton(label = 'Auto-save Config', underline = 11, variable = self.v_auto_save_config )
        self.menu_fichier.add_checkbutton(label = 'Auto-save Datas', underline = 11, variable = self.v_auto_save_data, state=tkinter.DISABLED  )
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
        self.menu_boutons = tkinter.Menu(self.menu_affichage, tearoff = 0)
        self.menu_affichage.add_cascade(label = 'Boutons', underline = 0, menu = self.menu_boutons)
        for button_frame_name in self.bts:
            self.menu_boutons.add_checkbutton(label = button_frame_name, variable = self.v_buttons_visible[button_frame_name], command = lambda: self.toggle_buttons_visible(button_frame_name))
        self.menu_affichage.add_checkbutton(label = 'Options-Résumé', underline = 0, variable = self.v_zone3_visible, command = self.toggle_zone3_visible)
        self.menu_affichage.add_checkbutton(label = 'Keypad', underline = 0, variable = self.v_keypad_visible, command = self.toggle_keypad_visible)
        self.menu_font = tkinter.Menu(self.menu_affichage, tearoff = 0)
        self.menu_affichage.add_cascade(label = "Font", menu = self.menu_font)
        for font in Fcalc.fonts:
            self.menu_font.add_radiobutton(label = str(font), variable = self.v_font, command = self.change_font)

        #Aide
        self.menu_aide = tkinter.Menu(self.menu_barre, tearoff =0)
        self.menu_barre.add_cascade(label = 'Aide', underline = 1, menu = self.menu_aide)
        self.menu_aide.add_command(label = 'A propos', underline = 0, command = self.about)
        self.menu_aide.add_command(label = 'Aide', underline = 1, command = self.help)
        self.menu_aide.add_command(label = 'Mises à jours...', underline = 0, command = self.check_update)
        self.window.config(menu = self.menu_barre)

        self.grid_buttons()
        self.grid_zone3()
        self.grid_keypad()
        self.window.columnconfigure(1, minsize = 200, weight = 2)
        self.window.rowconfigure(0, minsize = 100, weight = 1)
        self.zone2.rowconfigure(0, minsize = 100, weight = 1)


    def grid_buttons(self):
        grid_button = False
        for button_frame_name in self.bts:
            grid_button = grid_button or self.v_buttons_visible[button_frame_name].get()
        if grid_button:
            self.buttons.grid(column = 0, row = 0, rowspan =2, sticky = tkinter.N + tkinter.E + tkinter.W)
            self.window.columnconfigure(0, minsize = 120, weight = 1)
            for button_frame_name, v_button_frame in self.v_buttons_visible.items():
                if v_button_frame.get():
                    self.bts[button_frame_name].grid()
                else:
                    self.bts[button_frame_name].grid_forget()
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
    def grid_keypad(self):
        if self.v_keypad_visible.get():
            self.keypad.grid(column = 0, row = 2)
        else:
            self.keypad.grid_forget()

    def key_manager(self, event):
        ''' MAnage the key events
        '''
        logging.debug("Key pressed : '%s'"%event.keysym)
        if event.keysym in self.keys:
            f = self.keys[event.keysym]
            if f.delete1car: #TODO : bug quand CTRL-
                self.v_command_line.set(self.command_line()[0:-1])
            f._function()

    def do_keypad_event(self, txt):
        '''Do the ...
        '''
        logging.debug("Keypad %s pressed"%txt)
        if txt in self.keys:
            f = self.keys[txt]
            f._function()
        elif txt in [str(i) for i in range(10)]:
            self.v_command_line.set(self.v_command_line.get()+txt)
        elif txt == 'period':
            self.v_command_line.set(self.v_command_line.get()+'.')
        self.t_command_line.icursor(len(self.v_command_line.get()))

    def ctrlz(self, event):
        pass

    def command_line(self):
        '''Return the command line or None
        '''
        if len(self.v_command_line.get())==0:
            return None
        else:
            return self.v_command_line.get().replace(',','.')

    @staticmethod
    def about():
        tkinter.messagebox.showinfo("A propos de la calculatrice", \
            "Une calculatrice RPN (Polonaise inverse)\n \
            Auteur : FredThx\n \
            Version : %s\n \
            https://github.com/FredThx/FCALC"%__version__, \
            icon = 'info'
                    )
    def help(self):
        if self.url_help:
            webbrowser.open_new(self.url_help)

    def export(self):
        file = tkinter.filedialog.asksaveasfilename( \
                defaultextension = '.csv', \
                filetypes = [('Les valeurs (csv)', '*.csv')], \
                initialdir = self.path, \
                title = "Export Stack")
        if len(file)>0:
            result = self.stack.export_csv(file)
            if result == True:
                tkinter.messagebox.showinfo("Export Stack", "File %s created."%file)
            else:
                tkinter.messagebox.showerror("Export Stack", "%s"%result)

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
            print("self.stack.get()")
            self.stack.get()

    @staticmethod
    def toogle(v_val):
        if v_val.get():
            v_val.set(1)
        else:
            v_val.set(0)
    def toggle_buttons_visible(self, button_frame_name):
        self.toogle(self.v_buttons_visible[button_frame_name])
        self.grid_buttons()
    def toggle_zone3_visible(self):
        self.toogle(self.v_zone3_visible)
        self.grid_zone3()
    def toggle_keypad_visible(self):
        self.toogle(self.v_keypad_visible)
        self.grid_keypad()

    def change_font(self):
        '''When font change....
        '''
        self.stack.set_font()

    def save(self):
        '''Save all config to fcalc.json
        To be saved:
            -   v_buttons_visible
            -   v_zone3_visible
            -   v_keypad_visible
            -   v_keypad_visible
            -   self.window size
            - TODO : avec option : la stack
        '''
        params = {}
        params['buttons_visible'] = {}
        for button_frame_name in self.bts:
            params['buttons_visible'][button_frame_name] = self.v_buttons_visible[button_frame_name].get()
        params['zone3_visible'] = self.v_zone3_visible.get()
        params['keypad_visible'] = self.v_keypad_visible.get()
        params['font'] = self.v_font.get()
        params['window_geometry'] = self.window.geometry()
        params['options'] = self.options.params()
        params['path'] = self.path
        try:
            with open('fcalc.json', 'w') as f:
                json.dump(params, f)
        except Exception as e:
            logging.error(f"{e}")

    def load(self):
        '''Load fcalc.json if exist
        '''
        try:
            f = open("fcalc.json",'r')
            params = json.load(f)
            if 'auto_save_config' in params:
                self.v_auto_save_config.set(params['auto_save_config'])
            if 'auto_save_data' in params:
                self.v_auto_save_data.set(params['auto_save_data'])
            if 'buttons_visible' in params and type(params['buttons_visible'])== dict :
                for button_frame_name, value in params['buttons_visible'].items():
                    self.v_buttons_visible[button_frame_name].set(value)
            if 'zone3_visible' in params:
                self.v_zone3_visible.set(params['zone3_visible'])
            if 'keypad_visible' in params:
                self.v_keypad_visible.set(params['keypad_visible'])
            if 'font' in params:
                self.v_font.set(params['font'])
            if 'window_geometry' in params :
                self.window.geometry(params['window_geometry'])
            if 'options' in params:
                self.options.load(params['options'])
            if 'path' in params:
                self.path = params['path']
        except FileNotFoundError:
            pass

    def close(self):
        '''Close the App and save or not config
        '''
        if self.v_auto_save_config.get()==1:
            self.save()
        self.window.destroy()

    def check_update(self):
        '''Check for update on github
        '''
        github = Github(self.github_owner, self.github_repo)
        url_release = github.url_update(__version__)
        if url_release:
            if tkinter.messagebox.askokcancel("Nouvelle version disponible on Github","Voulez vous la télécharger?"):
                file = tkinter.filedialog.asksaveasfilename( \
                        filetypes = [('Fichier executable', '*.exe')], \
                        initialdir =  get_application_path(), \
                        initialfile = "fcalc.exe", \
                        title = "Enregistrer la nouvelle release (%s)"%url_release)
                if len(file)>0:
                    if os.path.exists(file):
                        if os.path.exists(file + '.bak'):
                            os.remove(file + ".bak")
                        os.rename(file, file + ".bak")
                    try:
                        destination_file = wget.download(url_release, file) #TODO : un peu d'animation
                        tkinter.messagebox.showinfo("Fcalc","Téléchargement réussit. L'application va redémarrer.")
                        os.system("start %s"%file)
                        self.close()
                    except:
                        logging.info("Error downloading %s"%url)
                        tkinter.messagebox.showerror("Fcalc","Erreur lors du téléchargement!")
