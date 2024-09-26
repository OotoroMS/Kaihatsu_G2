import tkinter as ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image,ImageTk
import DbCommunication as DMC #DB関係
db=DMC.DbCommunication()

def show_main_frm():
    main_frm.pack()
    work_mode_frm.pack_forget()
    admin_mode_frm.pack_forget()

def show_work_mode_frm():           #データ閲覧(data_view)に変更 
    main_frm.pack_forget()
    size_log_frm.pack_forget()
    vision_frm.pack_forget()
    work_mode_frm.pack()

def show_size_log_frm():
    work_mode_frm.pack_forget()
    size_log_frm.pack()
    show_size_log_graph()

def show_vision_frm():
    work_mode_frm.pack_forget()
    vision_frm.pack()

def show_admin_mode_frm():          #メンテナンス(maintenance)に変更
    main_frm.pack_forget()
    admin_mode_frm.pack()

def graph():
    
    size_list=[]
    result = db.table_data_get('testdb_02',"select * from DB_sizelog order by id desc limit 10")
    for i in result:
        size_list.append(i[2])

    size_show=list(reversed(size_list))#並び順を反対にしている
    x = [1,2,3,4,5,6,7,8,9,10]
    y = size_show
    yh = [0.075,0.075,0.075,0.075,0.075,0.075,0.075,0.075,0.075,0.075]
    yl = [-0.05,-0.05,-0.05,-0.05,-0.05,-0.05,-0.05,-0.05,-0.05,-0.05]

    fig = plt.Figure(figsize=(5,4))
    instance=fig.subplots()

    instance.plot(x,y)
    instance.plot(x,yh)
    instance.plot(x,yl)
    return fig

def show_size_log_graph():
    canvas = FigureCanvasTkAgg(graph(),master=size_log_frm)
    canvas.get_tk_widget().place(relx=0.2, rely=0.2)


def click_close():
    if messagebox.askokcancel("確認","終了しますか？"):
        rootform.destroy()

rootform = Tk()                                     #基盤ウィンドウ作成
rootform.title('test')                              #タイトル
rootform.geometry("900x600")                 #ウィンドウサイズ

#メインフレーム
main_frm = ttk.Frame(rootform,width=900,height=600)
main_frm.pack()

text1 = ttk.Label(main_frm,text="検査・蓄積収納装置",font=("",20))   #Label-テキスト
button1 = ttk.Button(main_frm,text="データ閲覧",
                     #style="sample.TButton",
                     command=show_work_mode_frm)      #Button-ボタン
button2 = ttk.Button(main_frm,text="メンテナンス",
                     #font=("",20),
                     command=show_admin_mode_frm)
textbox1 = ttk.Label(main_frm,text=
                     "・データ閲覧\n カウントログ\n 寸法検査ログ\n 外観検査ログ\n\n ・メンテナンス"
                     ,font=("",20))
buttonf = ttk.Button(main_frm,text="終了",command=click_close)

#配置 relx-x座標 rely-y座標 rewidth-幅 reheight-高さ  0.0~1.0
text1.place(relx=0.4, rely=0.05, relwidth=0.5, relheight=0.1)
button1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.2)
button2.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
textbox1.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.5)
buttonf.place(relx=0.7, rely=0.8, relwidth=0.1, relheight=0.1)

#作業者モードフレーム(データ閲覧に変更)
work_mode_frm = ttk.Frame(rootform,width=900,height=600)
work_mode_frm.pack()

text1 = ttk.Label(work_mode_frm,text="データ閲覧",font=("",20))
buttonc = ttk.Button(work_mode_frm,text="カウントログ",)             #c-count
buttons = ttk.Button(work_mode_frm,text="寸法検査ログ",
                     command=show_size_log_frm)             #s-size
buttone = ttk.Button(work_mode_frm,text="外観検査ログ",
                     command=show_vision_frm)       #e-exterior
buttonR = ttk.Button(work_mode_frm,text="戻る",command=show_main_frm)

text1.place(relx=0.4, rely=0.05, relwidth=0.5, relheight=0.1)
buttonc.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)
buttons.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)
buttone.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.1)
buttonR.place(relx=0.7, rely=0.8, relwidth=0.1, relheight=0.1)

#カウントログフレーム

#寸法検査ログフレーム
size_log_frm = ttk.Frame(rootform,width=900,height=600)
size_log_frm.pack()

buttonfig = ttk.Button(size_log_frm,text="fig",command=show_size_log_graph)
buttonR1 = ttk.Button(size_log_frm,text="戻る",command=show_work_mode_frm)

#buttonfig.pack()
#buttonR1.pack()
buttonfig.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.1)
buttonR1.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)


#外観検査ログフレーム
vision_frm = ttk.Frame(rootform,width=900,height=600)
vision_frm.pack()
buttonR1 = ttk.Button(vision_frm,text="戻る",command=show_work_mode_frm)
buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

img1=Image.open("真鍮_白黒画像/20240712_100033-01.jpg")
w_size = int(img1.width/4)
h_size = int(img1.height/4)
cvs=ttk.Canvas(vision_frm,width=w_size-2,height=h_size-2)
ttk_img=ImageTk.PhotoImage(image=img1.resize((w_size,h_size)))
cvs.create_image(0,0,image=ttk_img,anchor=ttk.NW)
cvs.place(relx=0.07,rely=0.08,anchor=ttk.NW)

#管理者モードフレーム(メンテナンスに変更)
admin_mode_frm = ttk.Frame(rootform,width=900,  height=600)
admin_mode_frm.pack()

text1 = ttk.Label(admin_mode_frm,text="メンテナンス",font=("",20))
buttonM1 = ttk.Button(admin_mode_frm,text="メンテナンス1")
buttonM2 = ttk.Button(admin_mode_frm,text="メンテナンス2")
buttonM3 = ttk.Button(admin_mode_frm,text="メンテナンス3")
buttonM4 = ttk.Button(admin_mode_frm,text="メンテナンス4")
buttonM5 = ttk.Button(admin_mode_frm,text="メンテナンス5")
buttonM6 = ttk.Button(admin_mode_frm,text="メンテナンス6")
buttonR2 = ttk.Button(admin_mode_frm,text="戻る",command=show_main_frm)

text1.place(relx=0.4, rely=0.05, relwidth=0.5, relheight=0.1)
buttonR2.place(relx=0.7, rely=0.8, relwidth=0.1, relheight=0.1)

show_main_frm()

rootform.protocol("WM_DELETE_WINDOW",click_close)
rootform.mainloop()