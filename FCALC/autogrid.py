# coding: utf8

'''
Un Frame tkinter
    auquel on peut ajouter des widgets qui se positionent en carre
Usage :
    cf __main__
'''
import tkinter
import logging

class AutoGrid(tkinter.Frame):
    def __init__(self, master = None, **kwargs):
        tkinter.Frame.__init__(self, master, **kwargs)
        self.columns = 0
        self.bind('<Configure>', self.regrid)

    def regrid(self, event=None):
        width = self.winfo_width()
        logging.debug("%s.width : %s"%(self, width))
        slaves = self.grid_slaves()
        logging.debug("slaves : %s"%( slaves))
        max_width = max(slave.winfo_width() for slave in slaves)
        logging.debug("max_width : %s"%(max_width))
        cols = width // max_width
        if cols == self.columns: # if the column number has not changed, abort
            return
        for i, slave in enumerate(slaves):
            slave.grid_forget()
            slave.grid(row=i//cols, column=i%cols)
        self.columns = cols


if __name__ == '__main__':
    root = tkinter.Tk()
    frame = AutoGrid(root)
    frame.pack(fill=tkinter.BOTH, expand=True)

    tkinter.Button(frame, text="1").grid() # use normal grid parameters to set up initial layout
    tkinter.Button(frame, text="2").grid(column=1)
    tkinter.Button(frame, text="333333").grid(column=2)
    tkinter.Button(frame, text="4").grid()
    tkinter.Button(frame, text="5").grid()
    tkinter.Button(frame, text="6").grid()
    root.mainloop()
