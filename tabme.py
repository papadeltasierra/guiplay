from tkinter import *
from tkinter import ttk

root = Tk()

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

Grid.columnconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 0, weight=1)

tabControl.add(tab1, text ='Tab 1')
tabControl.add(tab2, text ='Tab 2')
tabControl.grid(row=0, column=0, sticky='nsew')


tab1.columnconfigure( (0,1), weight=1)
tab1.rowconfigure((0,1), weight=1)

lbl1 = Label(tab1, text='This is frame 1')
lbl2 = Label(tab1, text='This is frame 2')
lbl3 = Label(tab1, text='This is frame 3')
lbl4 = Label(tab1, text='This is frame 4')

lbl1.grid(row=0, column=0)
lbl2.grid(row=0, column=1)
lbl3.grid(row=1, column=0)
lbl4.grid(row=1, column=1)


root.mainloop()