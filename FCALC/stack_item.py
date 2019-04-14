# coding: utf8

'''
Un Label tkinter
    qui représente un item de la stack
Usage :
'''
import tkinter as tkinter
import logging

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
        tkinter.Label.__init__(self, stack.interior, textvariable = self.v_text, width = 25, anchor = 'sw',justify = 'right')
        #Menu contextuel
        self.aMenu = tkinter.Menu(self, tearoff = 0)
        self.aMenu.add_command(label = 'Drop', command = self.delete)
        self.aMenu.add_command(label = 'Dup', command = self.duplicate)
        self.aMenu.add_command(label = 'Copy', command = lambda: self.stack.copy_to_clipboard(self))
        self.aMenu.add_command(label = 'Cut', command = lambda: self.stack.cut_to_clipboard(self))

        #Evenements
        self.bind('<Double-Button-1>', lambda event : self.duplicate())
        self.bind('<Double-Button-3>', lambda event : self.delete())
        self.bind('<Button-3>', self.popup_menu)
        self.bind("<ButtonPress-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        self.configure(cursor = "hand1")



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

    def duplicate(self):
        '''Copy the item to the last position in the stack
        '''
        self.stack.put_items(self.clone())

    def delete(self):
        '''Delete the item from the stack
        '''
        self.stack.del_items(self)

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
        if self.function:
            return self.args
        else:
            return (self,)
    #DRAG and DROP methods
    def on_drag_start(self, event):
        self.config(background  = '#FFFFCC')
        logging.debug("Drag start for %s"%self)

    def on_drag(self, event):
        x,y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x,y)
        if isinstance(target, StackItem) and target is not self:
            logging.debug("Move %s to %s"%(self, target))
            my_row = self.grid_info()['row']
            target_row = target.grid_info()['row']
            self.grid(row = target_row)
            target.grid(row = my_row)
            self.stack.move(self, target_row)


    def on_drop(self, event):
        logging.debug("Dropfor %s event : %s"%(self,event))
        self.config(background  = 'SystemButtonFace')

    def popup_menu(self, event):
        '''Show the context menu
        '''
        self.aMenu.post(event.x_root, event.y_root)
