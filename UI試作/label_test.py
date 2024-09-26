import tkinter as tki
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image,ImageTk
from pathlib import Path
import os
import os.path
import time

class test():
    def __init__(self):
        self.root = tki.Tk()
        self.root.title("label test")
        self.root.geometry("1920x1080")

        self.main = None
        
        self.label_text_01 = tki.StringVar()
        self.label_text_02 = "OK"
        self.cnt=0

    def _create_main(self):
        self.main = tki.Frame(self.root,width=1920,height=1080)
        self.main.pack()

        label_title = tki.Label(self.main,
                               text="ラベル更新テスト",
                               font=("",70))
        #   setを使用
        label_test01 = tki.Label(self.root,
                                 textvariable=self.label_text_01,
                                 font=("",60))
        #   代入を使用
        label_test02 = tki.Label(self.root,
                                 textvariable=self.label_text_02,
                                 font=("",60))
        
        label_title.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
        label_test01.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.2)
        label_test02.place(relx=0.5, rely=0.3, relwidth=0.3, relheight=0.2)
        self.root.after(3000, self._label_update)    
    
    def _label_update(self):
        if self.label_text_01.get() == ("OK"):
            self.label_text_01.set("NG")
            self.label_text_02 = "NG"
        else:
            self.cnt+=1
            self.label_text_01.set(self.cnt)
            self.label_text_02 = "OK"
        self.root.after(3000, self._label_update)
        
    def start(self):
        self._create_main()
        self.root.mainloop()

if __name__ == "__main__":
    gui = test()
    gui.start()