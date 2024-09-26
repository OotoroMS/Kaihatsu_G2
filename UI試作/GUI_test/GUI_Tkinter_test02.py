import sys
from tkinter import *
from tkinter import messagebox
import tkinter as ttk
from PIL import Image,ImageTk #jpgに対応するため
#import pathlib #画像取得のfile関係()
import DbCommunication as DMC #DB関係
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import tkinter.ttk as ttk

def show_main_frm():
    #main_frm.place(relx=0.01,rely=0.01,anchor=ttk.NW)#--placeで統一する
    #.place(width:幅,height:高さ,x:横の位置,y:縦の位置)
    main_frm.place(anchor=ttk.NW)#--anchor:アンカー,どこを基準にするかNW:北西
    work_mode_frm.place_forget()
    admin_mode_frm.place_forget()

def show_work_mode_frm():
    main_frm.place_forget()
    vision_frm.place_forget()
    work_mode_frm.place(anchor=ttk.NW)

def show_admin_mode_frm():
    main_frm.place_forget()
    admin_mode_frm.place(anchor=ttk.NW)

def show_vision_frm():
    work_mode_frm.place_forget()
    vision_frm.place(anchor=ttk.NW)

def end():
    sys.exit()

rootform = ttk.Tk()                    #基盤ウィンドウ作成
rootform.title('test')                  #タイトル
rootform.geometry("900x600+0+0")     #ウィンドウサイズ(横幅*高さ+ｘ座標+ｙ座標)

#メインフレーム------------------------------------------------------
main_frm = ttk.Frame(rootform,width=900,height=600,bg='green')#root → rootform,bg='green'

text1 = ttk.Label(main_frm,text="検査・蓄積収納装置",font=("Helvetica",45)).place(relx=0.21,rely=0.05,anchor=ttk.NW)   #Label-テキスト
text2 = ttk.Label(main_frm,text="メインメニュー",font=("Helvetica",10)).place(relx=0.01,rely=0.01,anchor=ttk.NW)   #Label-テキスト
button1 = ttk.Button(main_frm,text="データ閲覧",font=("",35),command=show_work_mode_frm).place(relx=0.17,rely=0.35,anchor=ttk.NW)    #Button-ボタン
button2 = ttk.Button(main_frm,text="メンテナンス",font=("",35),command=show_admin_mode_frm).place(relx=0.17,rely=0.55,anchor=ttk.NW)
button2 = ttk.Button(main_frm,text="終了",font=("",20),command=end).place(relx=0.8,rely=0.8,anchor=ttk.NW)
textbox1 = ttk.Label(main_frm,text="動作状況：正常",font=("",20)).place(relx=0.2,rely=0.8,anchor=ttk.NW)

db=DMC.DbCommunication()#DB用
db.db_list_display()
size_list=[]
result = db.table_data_get('testdb_02',"select * from DB_sizelog")
#for i in result:
#    num02=i[2]#dayの値を取得

#作業者モードフレーム------------------------------------------------------
work_mode_frm = ttk.Frame(rootform,width=900,height=600,bg='blue')

text1 = ttk.Label(work_mode_frm,text="作業者モード",font=("",30)).place(relx=0.2,rely=0.05)
buttonV = ttk.Button(work_mode_frm,text="外観写真",font=("",20),command=show_vision_frm).place(relx=0.2,rely=0.2)
buttonR = ttk.Button(work_mode_frm,text="戻る",font=("",20),command=show_main_frm).place(relx=0.2,rely=0.4)


#管理者モードフレーム------------------------------------------------------
admin_mode_frm = ttk.Frame(rootform,width=900,height=600,bg='red')

text1 = ttk.Label(admin_mode_frm,text="管理者モード").place(relx=0.1,rely=0.1)
buttonR2 = ttk.Button(admin_mode_frm,text="戻る",font=("",20),command=show_main_frm).place(relx=0.1,rely=0.2)

#外観写真フレーム------------------------------------------------------
vision_frm = ttk.Frame(rootform,width=900,height=600,bg='white')

buttonR3 = ttk.Button(vision_frm,text="戻る",font=("",20),command=show_work_mode_frm).place(relx=0.7,rely=0.7)
#img1=Image.open("真鍮_白黒画像/20240712_100033-01.jpg")
#w_size = int(img1.width/4)
#h_size = int(img1.height/4)
#cvs=ttk.Canvas(vision_frm,width=w_size-2,height=h_size-2)
#ttk_img=ImageTk.PhotoImage(image=img1.resize((w_size,h_size)))
#cvs.create_image(0,0,image=ttk_img,anchor=ttk.NW)
#cvs.place(relx=0.13,rely=0.1,anchor=ttk.NW)
fig=Figure(figsize=(5,4))#dpi=100
ax = fig.add_subplot(111)
#ax.set_xlim(-1,1)
#ax.set_ylim(-1,1)

canvas=FigureCanvasTkAgg(fig,vision_frm)
#toolbar=NavigationToolbar2Tk(canvas,vision_frm)
canvas.draw()
canvas.get_tk_widget().place(relx=0.1,rely=0.1,anchor=ttk.NW)

show_main_frm()

rootform.mainloop()