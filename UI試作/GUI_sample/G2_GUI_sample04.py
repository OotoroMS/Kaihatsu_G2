import tkinter as ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image,ImageTk
import DbCommunication_old as DMC #DB関係
from pathlib import Path
import os
import os.path
db=DMC.DbCommunication()
import time

def show_main_frm():
    main_frm.pack()
    work_mode_frm.pack_forget()
    admin_mode_frm.pack_forget()
    size_log_frm.pack_forget()
    vision_frm.pack_forget()

def show_work_mode_frm():           #データ閲覧(data_view)に変更 
    main_frm.pack_forget()
    size_log_frm.pack_forget()
    vision_frm.pack_forget()
    work_mode_frm.pack()
    global flag_01
    flag_01=0
    global flag_02
    flag_02=0

def show_size_log_frm():
    work_mode_frm.pack_forget()
    size_log_frm.pack()
    global flag_02
    flag_02=1
    show_size_log_graph()
    vision_frm.pack_forget()

def show_vision_frm():
    work_mode_frm.pack_forget()
    size_log_frm.pack_forget()
    vision_frm.pack()
    global flag_01
    flag_01=1
    vision_up()

def show_admin_mode_frm():          #メンテナンス(maintenance)に変更
    main_frm.pack_forget()
    admin_mode_frm.pack()
    size_log_frm.pack_forget()
    vision_frm.pack_forget()

def graph():
    
    size_list=[]#データベースから値を取得
    result = db.table_data_get('testdb_02',"select * from DB_sizelog order by id desc limit 10")
    for i in result:
        size_list.append(i[2])

    size_show=list(reversed(size_list))#並び順を反対にしている
    x = [1,2,3,4,5,6,7,8,9,10]
    y = size_show
    yh = []#上限
    yl = []#下限
    for i in range(0,10,1):
        yh.append(0.1)
        yl.append(-0.1)

    fig = plt.Figure(figsize=(5,4))
    instance=fig.subplots()

    instance.plot(x,y)
    instance.plot(x,yh)
    instance.plot(x,yl)
    print("graph_run")
    return fig

def show_size_log_graph():
    canvas = FigureCanvasTkAgg(graph(),master=size_log_frm)
    canvas.get_tk_widget().place(relx=0.2, rely=0.2)
    global flag_02
    ut=time.time()
    print(ut)
    if(flag_02 == 1):
        rootform.after(5000,show_size_log_graph) #画面が点滅するのを解消したい

def click_close():
    if messagebox.askokcancel("確認","終了しますか？"):
        rootform.destroy()

def vision_up():
    dir_path = Path("D:/GitHub/Kaihatsu_G2/UI試作/真鍮_白黒画像")
    files = list(dir_path.glob("*.jpg"))
    print(len(files))

    list_date=[]
    for i in range(len(files)):
        file_name, ext = os.path.splitext(files[i].name)
        list_date.append(file_name)
    print(list_date)
    
    list_date_sort=sorted(list_date,reverse=True)
    list_date_new=list_date_sort[0]
    print(list_date_new)
    img1=Image.open("D:/GitHub/Kaihatsu_G2/UI試作/真鍮_白黒画像/"f"/{list_date_new}.jpg")
    w_size = int(img1.width/4)
    h_size = int(img1.height/4)
    global ttk_img
    ttk_img=ImageTk.PhotoImage(image=img1.resize((w_size,h_size))) # Pillowで読み込んだ画像をtkinterで表示できるよう設定
    cvs=ttk.Canvas(vision_frm,width=w_size-2,height=h_size-2,bg="red")# tkinterは標準でJPEGを表示できないため
    cvs.create_image(0,0,image=ttk_img,anchor=ttk.NW)
    cvs.place(relx=0.07,rely=0.08,anchor=ttk.NW)

    #rootform.after(1000,vision_up)#1秒ごとに処理
    print(flag_01)
    if(flag_01 == 1):
        rootform.after(1000,vision_up)#1秒ごとに処理


rootform = Tk()                                     #基盤ウィンドウ作成
rootform.title('test')                              #タイトル
rootform.geometry("900x600")                 #ウィンドウサイズ#900×600 1920×600

flag_01=0

#メインフレーム
main_frm = ttk.Frame(rootform,width=900,height=600)#bg="blue"
main_frm.pack()

text1 = ttk.Label(main_frm,text="検査・蓄積収納装置",font=("",20))   #Label-テキスト
button1 = ttk.Button(main_frm,text="データ閲覧",
                     #style="sample.TButton",
                     font=("",20),
                     command=show_work_mode_frm)      #Button-ボタン
button2 = ttk.Button(main_frm,text="メンテナンス",
                     font=("",20),
                     command=show_admin_mode_frm)
textbox1 = ttk.Label(main_frm,text=
                     "・データ閲覧\n カウントログ \n寸法検査ログ\n外観検査ログ\n\n ・メンテナンス"
                     ,font=("",20))
buttonf = ttk.Button(main_frm,text="終了",command=click_close)

#配置 relx-x座標 rely-y座標 rewidth-幅 reheight-高さ  0.0~1.0
text1.place(relx=0.4, rely=0.05, relwidth=0.5, relheight=0.1)
button1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.2)
button2.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
textbox1.place(relx=0.6, rely=0.2)#, relwidth=0.3, relheight=0.5
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

#buttonfig = ttk.Button(size_log_frm,text="fig",command=show_size_log_graph)
buttonR1 = ttk.Button(size_log_frm,text="戻る",command=show_work_mode_frm)

#buttonfig.pack()
#buttonR1.pack()
#buttonfig.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.1)
buttonR1.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)


#外観検査ログフレーム
vision_frm = ttk.Frame(rootform,width=900,height=600)
vision_frm.pack()
buttonR1 = ttk.Button(vision_frm,text="戻る",command=show_work_mode_frm)
buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

#管理者モードフレーム(メンテナンスに変更)
admin_mode_frm = ttk.Frame(rootform,width=900,  height=600)#bg="red"
admin_mode_frm.pack()

text1 = ttk.Label(admin_mode_frm,text="メンテナンス",font=("",20))
buttonM1 = ttk.Button(admin_mode_frm,text="メンテナンス1")
buttonM2 = ttk.Button(admin_mode_frm,text="メンテナンス2")
buttonM3 = ttk.Button(admin_mode_frm,text="メンテナンス3")
buttonM4 = ttk.Button(admin_mode_frm,text="メンテナンス4")
buttonM5 = ttk.Button(admin_mode_frm,text="メンテナンス5")
buttonM6 = ttk.Button(admin_mode_frm,text="メンテナンス6")
buttonR2 = ttk.Button(admin_mode_frm,text="戻る",command=show_main_frm)

text1.place(relx=0, rely=0.05, relwidth=0.2, relheight=0.1)
buttonR2.place(relx=0.7, rely=0.8, relwidth=0.1, relheight=0.1)

show_main_frm()

rootform.protocol("WM_DELETE_WINDOW",click_close)
rootform.mainloop()