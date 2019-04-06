# coding: utf8

'''
Un Frame tkinter
    auquel on peut ajouter des widgets qui se positionent en carre
Usage :
    cf __main__
'''
import tkinter as tk

class AutoGrid(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.columns = None
        self.bind('<Configure>', self.regrid)

    def regrid(self, event=None):
        width = self.winfo_width()
        slaves = self.grid_slaves()
        print(slaves)
        max_width = max(slave.winfo_width() for slave in slaves)
        cols = width // max_width
        if cols == self.columns: # if the column number has not changed, abort
            return
        for i, slave in enumerate(slaves):
            slave.grid_forget()
            slave.grid(row=i//cols, column=i%cols)
        self.columns = cols


if __name__ == '__main__':
    root = tk.Tk()
    frame = AutoGrid(root)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Button(frame, text="1").grid() # use normal grid parameters to set up initial layout
    tk.Button(frame, text="2").grid(column=1)
    tk.Button(frame, text="333333").grid(column=2)
    tk.Button(frame, text="4").grid()
    tk.Button(frame, text="5").grid()
    tk.Button(frame, text="6").grid()
    root.mainloop()
