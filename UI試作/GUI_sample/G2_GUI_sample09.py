#   変更・改善点：　カウントログの表の表示を調整
import tkinter as tki
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image,ImageTk
import DbCommunication as DMC #DB関係
from pathlib import Path
import os
import os.path
db=DMC.DbCommunication()
import time

global CANCEL_FLG

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
    count_frm.pack_forget()
    work_mode_frm.pack()
    global flag_01
    flag_01=0
    global flag_02
    flag_02=0
    global flag_03
    flag_03=0

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
    ut=time.time()#動作確認用
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
    cvs=tki.Canvas(vision_frm,width=w_size-2,height=h_size-2,bg="red")# tkinterは標準でJPEGを表示できないため
    cvs.create_image(0,0,image=ttk_img,anchor=tki.NW)
    cvs.place(relx=0.07,rely=0.08,anchor=tki.NW)

    #rootform.after(1000,vision_up)#1秒ごとに処理
    print(flag_01)
    if(flag_01 == 1):
        rootform.after(1000,vision_up)#1秒ごとに処理

def show_count_frm():  #メンテナンス(maintenance)に変更
    work_mode_frm.pack_forget()
    count_frm.pack()
    global flag_03
    global flag_today
    global flag_7days
    global CANCEL_FLG
    global tree
    CANCEL_FLG = None
    flag_03=1
    flag_today = 1
    flag_7days = 0
    tree = None
    size_log_frm.pack_forget()
    vision_frm.pack_forget()
    count_log()
    # count_log_7_days()

def count_log_7_days():
    global CANCEL_FLG
    global tree
    #   当日のカウントログ表示の自動更新設定を解除
    if CANCEL_FLG != None:
        rootform.after_cancel(CANCEL_FLG)
    if tree != None:
        tree.destroy()
        
    #   表のクラスを生成
    tree=ttk.Treeview(count_frm,column=('days','NO','good_size','bad_size','good_vision','bad_vision'),show='headings')
    
    #   表の書式を設定
    style = ttk.Style()
    style.configure('Treeview.Heading',font=("",20))
    style.configure('Treeview',rowheight=50,font=("",30)) 
    #   カラムを設定
    tree.column('days',width=140,anchor='center')
    tree.column('NO',width=140,anchor='center')
    tree.column('good_size',width=140,anchor='center')
    tree.column('bad_size',width=140,anchor='center')
    tree.column('good_vision',width=140,anchor='center')
    tree.column('bad_vision',width=140,anchor='center')
    #   ヘッダーを設定
    tree.heading('days',text='日付',anchor='center')
    tree.heading('NO',text='総個数',anchor='center')
    tree.heading('good_size',text='寸法良',anchor='center')
    tree.heading('bad_size',text='寸法不良',anchor='center')
    tree.heading('good_vision',text='外観良',anchor='center')
    tree.heading('bad_vision',text='外観不良',anchor='center')
    #   結果を取得
    result = db.table_data_get('testdb_02',"select * from db_countlog order by id DESC limit 7")
    #   iに結果を代入し、表に代入
    for i in result:
        print(i)#i[0]-[5]:[0]id,[1]day,[2]good_size,[3]good_vision,[4]bad_size,[5]bad_vision
        #   試作
        if type(i[1]) == str:
            day = ""
            for size in range((len(i[1]) - 5)):
                day = day + (i[1][size + 5])
            print(day)
            tree.insert(parent='',index='end',values=(day,i[2]+i[4],i[2],i[4],i[3],i[5]))
    #   表を配置
    tree.place(width=870,height=500,relx=0.02,rely=0.02,anchor=tki.NW)
    #   ﾌﾗｸﾞが立っていたら
    if(flag_03 == 1):
        CANCEL_FLG = rootform.after(5000,count_log_7_days) #画面が点滅するのを解消したい
        

def count_log():
    global CANCEL_FLG
    global tree
    #   七日間の記録の表示自動更新を解除
    if CANCEL_FLG != None:
        rootform.after_cancel(CANCEL_FLG)
        
    
    if tree != None:
        tree.destroy()
    
    tree=ttk.Treeview(count_frm,column=('NO','good_size','bad_size','good_vision','bad_vision'),show='headings')

    style = ttk.Style()
    style.configure('Treeview.Heading',font=("",30))
    style.configure('Treeview',font=("",30))
    
    tree.column('NO',width=150,anchor='center')
    tree.column('good_size',width=150,anchor='center')
    tree.column('bad_size',width=150,anchor='center')
    tree.column('good_vision',width=150,anchor='center')
    tree.column('bad_vision',width=150,anchor='center')

    tree.heading('NO',text='総個数',anchor='center')
    tree.heading('good_size',text='寸法良',anchor='center')
    tree.heading('bad_size',text='寸法不良',anchor='center')
    tree.heading('good_vision',text='外観良',anchor='center')
    tree.heading('bad_vision',text='外観不良',anchor='center')

    result = db.table_data_get('testdb_02',"select * from db_now")
    for i in result:
        print(i)#i[0]-[5]:[0]id,[1]day,[2]good_size,[3]good_vision,[4]bad_size,[5]bad_vision

    tree.insert(parent='',index='end',values=(i[2]+i[4],i[2],i[4],i[3],i[5]))

    tree.place(width=870,height=150,relx=0.02,rely=0.02,anchor=tki.NW)

    if(flag_03 == 1):
        CANCEL_FLG = rootform.after(5000,count_log) #画面が点滅するのを解消したい
        


rootform = Tk()                                     #基盤ウィンドウ作成
rootform.title('test')                              #タイトル
rootform.geometry("900x600")                 #ウィンドウサイズ#900×600 1920×600


#メインフレーム
main_frm = tki.Frame(rootform,width=900,height=600)#bg="blue"
main_frm.pack()

text1 = tki.Label(main_frm,text="検査・蓄積収納装置",font=("",20))   #Label-テキスト
button1 = tki.Button(main_frm,text="データ閲覧",
                     #style="sample.TButton",
                     font=("",20),
                     command=show_work_mode_frm)      #Button-ボタン
button2 = tki.Button(main_frm,text="メンテナンス",
                     font=("",20),
                     command=show_admin_mode_frm)
textbox1 = tki.Label(main_frm,text=
                     "・データ閲覧\n カウントログ \n寸法検査ログ\n外観検査ログ\n\n ・メンテナンス"
                     ,font=("",20))
buttonf = tki.Button(main_frm,text="終了",command=click_close)

#配置 relx-x座標 rely-y座標 rewidth-幅 reheight-高さ  0.0~1.0
text1.place(relx=0.4, rely=0.05, relwidth=0.5, relheight=0.1)
button1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.2)
button2.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
textbox1.place(relx=0.6, rely=0.2)#, relwidth=0.3, relheight=0.5
buttonf.place(relx=0.7, rely=0.8, relwidth=0.1, relheight=0.1)

#作業者モードフレーム(データ閲覧に変更)
work_mode_frm = tki.Frame(rootform,width=900,height=600)
work_mode_frm.pack()

text1 = tki.Label(work_mode_frm,text="データ閲覧",font=("",20))
buttonc = tki.Button(work_mode_frm,text="カウントログ",
                     command=show_count_frm)             #c-count
buttons = tki.Button(work_mode_frm,text="寸法検査ログ",
                     command=show_size_log_frm)             #s-size
buttone = tki.Button(work_mode_frm,text="外観検査ログ",
                     command=show_vision_frm)       #e-exterior
buttonR = tki.Button(work_mode_frm,text="戻る",command=show_main_frm)

text1.place(relx=0.4, rely=0.05, relwidth=0.5, relheight=0.1)
buttonc.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)
buttons.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)
buttone.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.1)
buttonR.place(relx=0.7, rely=0.8, relwidth=0.1, relheight=0.1)

#寸法検査ログフレーム
size_log_frm = tki.Frame(rootform,width=900,height=600)
size_log_frm.pack()

#buttonfig = tki.Button(size_log_frm,text="fig",command=show_size_log_graph)
buttonR1 = tki.Button(size_log_frm,text="戻る",command=show_work_mode_frm)

#buttonfig.pack()
#buttonR1.pack()
#buttonfig.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.1)
buttonR1.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)


#外観検査ログフレーム
vision_frm = tki.Frame(rootform,width=900,height=600)
vision_frm.pack()
buttonR1 = tki.Button(vision_frm,text="戻る",command=show_work_mode_frm)
buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

#カウントログフレーム
count_frm = tki.Frame(rootform,width=900,height=600)
count_frm.pack()
button_cr_today = tki.Button(count_frm,text="本日の記録",command=count_log)
button_cr_7days = tki.Button(count_frm,text="火の七日間",command=count_log_7_days)
buttonR3 = tki.Button(count_frm,text="戻る",command=show_work_mode_frm)
buttonR3.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
button_cr_today.place(relx=0.1,rely=0.85, relwidth=0.1, relheight=0.1)
button_cr_7days.place(relx=0.3,rely=0.85, relwidth=0.1, relheight=0.1)
#管理者モードフレーム(メンテナンスに変更)
admin_mode_frm = tki.Frame(rootform,width=900,  height=600)#bg="red"
admin_mode_frm.pack()

text1 = tki.Label(admin_mode_frm,text="メンテナンス",font=("",20))
buttonM1 = tki.Button(admin_mode_frm,text="メンテナンス1")
buttonM2 = tki.Button(admin_mode_frm,text="メンテナンス2")
buttonM3 = tki.Button(admin_mode_frm,text="メンテナンス3")
buttonM4 = tki.Button(admin_mode_frm,text="メンテナンス4")
buttonM5 = tki.Button(admin_mode_frm,text="メンテナンス5")
buttonM6 = tki.Button(admin_mode_frm,text="メンテナンス6")
buttonR2 = tki.Button(admin_mode_frm,text="戻る",command=show_main_frm)

text1.place(relx=0, rely=0.05, relwidth=0.2, relheight=0.1)
buttonR2.place(relx=0.7, rely=0.8, relwidth=0.1, relheight=0.1)

show_main_frm()

rootform.protocol("WM_DELETE_WINDOW",click_close)
rootform.mainloop()