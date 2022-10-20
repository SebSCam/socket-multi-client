from tkinter import *
import os
import re
import server

class ViewServer(Frame):

    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.parent = master
        self.grid()
        #self.createWidgets()



    def __initComponents(self):
        self.frame = Frame(height=500,width=750)
        self.frame.grid_propagate(False)
        self.frame.pack(expand=1)