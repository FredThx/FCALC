# -*- coding: ISO-8859-1 -*-
import tkinter as tk

class InfoBulle(tk.Toplevel):
	def __init__(self,parent=None,texte='',temps=1000, max_lenght = 25):
		tk.Toplevel.__init__(self,parent,bd=1,bg='black')
		self.tps=temps
		self.parent=parent
		self.withdraw()
		self.overrideredirect(1)
		self.transient()
		if len(texte)> max_lenght:
			texte = texte[:max_lenght] + "..."
		l=tk.Label(self,text=texte,bg="yellow",justify='left')
		l.update_idletasks()
		l.pack()
		l.update_idletasks()
		self.tipwidth = l.winfo_width()
		self.tipheight = l.winfo_height()
		self.parent.bind('<Enter>',self.delai)
		self.parent.bind('<Button-1>',self.efface)
		self.parent.bind('<Leave>',self.efface)
	def delai(self,event):
		self.action=self.parent.after(self.tps,self.affiche)
	def affiche(self):
		self.update_idletasks()
		posX = self.parent.winfo_rootx()+20
		posY = self.parent.winfo_rooty()-int(self.parent.winfo_height())
		#~ print posX,print posY
		self.geometry('+%d+%d'%(posX,posY))
		self.deiconify()
	def efface(self,event):
		self.withdraw()
		self.parent.after_cancel(self.action)

if __name__ == '__main__':
	root = tk.Tk()
	lab1=tk.Label(root,text='Infobulle 1')
	lab1.pack()
	lab2=tk.Label(root,text='Infobulle 2')
	lab2.pack()
	i1 = InfoBulle(parent=lab1,texte="Infobulle 1")
	i2= InfoBulle(parent=lab2,texte="Infobulle 2")
	root.mainloop()
