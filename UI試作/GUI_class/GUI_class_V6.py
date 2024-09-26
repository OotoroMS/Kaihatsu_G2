#   命名者 原　京平 学籍番号 2321321
import tkinter as tk
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
import time

class GUI():
    #   初期化
    def __init__(self):
        self.rootform = tk.Tk()
        self.rootform.title('test')
        self.rootform.geometry("1920x1080")#900x600,1920x1080
        #   各フレーム初期化
        self.main_frm = None
        self.work_mode_frm = None
        self.admin_mode_frm = None
        self.size_log_frm = None
        self.vision_frm = None
        self.count_frm = None
        #   データベース関係
        self.db=DMC.DbCommunication()
        #   自動更新関係
        self.cansel_id = None
        self.tree  = None
        self.canvas = None
        self.display_label = None
        #   稼働状況関係
        self.vitals_msg = None
        self.vitals_flg = None

        self.show_main_frm()
        self.rootform.protocol("WM_DELETE_WINDOW",self.click_close)
        self.rootform.mainloop()

    #   メインフレーム生成
    def main_frm_create(self):
        self.main_frm = tk.Frame(self.rootform, width=1920,height=1080)
        self.main_frm.pack()
        
        self.vitals_msg = "稼働中"#--------------------稼働状況のメッセージ

        #   テキストの設定
        text1 = tk.Label(self.main_frm,text="検査・蓄積収納装置", font=("",60))
        
        #   ボタン生成
        button1 = tk.Button(self.main_frm,text="データ閲覧",
                            #style="sample.TButton",
                            font=("",50),
                            command=self.show_work_mode_frm)      #Button-ボタン
        button2 = tk.Button(self.main_frm,text="メンテナンス",
                            font=("",50),
                            command=self.show_admin_mode_frm)
        textbox1 = tk.Label(self.main_frm,text=
                            "・データ閲覧\n カウントログ \n寸法検査ログ\n外観検査ログ\n\n ・メンテナンス"
                            ,font=("",40))
        buttonf = tk.Button(self.main_frm,text="終了",
                            font=("",40),
                            command=self.click_close)
        buttont = tk.Button(self.main_frm,text="テスト",
                            font=("",40),
                            command=self.test)
        
        self.main_vitals = tk.Label(self.main_frm,text=self.vitals_msg,
                                font=("",30),relief=tk.SOLID)

        text1.place(relx=0.22, rely=0.05, relwidth=0.5, relheight=0.1)
        button1.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.2)
        button2.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
        textbox1.place(relx=0.6, rely=0.3)#, relwidth=0.3, relheight=0.5
        buttonf.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
        self.main_vitals.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.1)
        buttont.place(relx=0.75, rely=0.3)

        # self.main_vital_flg =  self.rootform.after(1000,self.vitals_update)
        self.vital_update(self.main_vitals)
        self.rootform.after(5000,self.test)#テスト用メッセージ自動切換え

    #   メインフレーム削除
    def main_frm_destroy(self):
        if self.main_frm != None:
            self.main_frm.destroy()
            self.main_frm = None
    
    #   作業者用モードフレーム生成
    def work_mode_frm_create(self):
        self.work_mode_frm = tk.Frame(self.rootform,width=1920,height=1080)
        self.work_mode_frm.pack()

        #   部品生成
        text1 = tk.Label(self.work_mode_frm,text="データ閲覧",font=("",70))
        buttonc = tk.Button(self.work_mode_frm,text="カウントログ",font=("",50),command=self.show_count_frm)             #c-count
        buttons = tk.Button(self.work_mode_frm,text="寸法検査ログ",font=("",50),command=self.show_size_log_frm)             #s-size
        buttone = tk.Button(self.work_mode_frm,text="外観検査ログ",font=("",50),command=self.show_vision_frm)       #e-exterior
        buttonR = tk.Button(self.work_mode_frm,text="戻る",font=("",40),command=self.work_mode_frm_finish)
        
        self.work_vitals = tk.Label(self.work_mode_frm,text=self.vitals_msg,
                                        font=("",30),relief=tk.SOLID)

        #   配置
        text1.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
        buttonc.place(relx=0.1, rely=0.25, relwidth=0.3, relheight=0.1)
        buttons.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.1)
        buttone.place(relx=0.1, rely=0.65, relwidth=0.3, relheight=0.1)
        buttonR.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
        self.work_vitals.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.1)

        self.vital_update(self.work_vitals)
    
    #   作業者湯モードフレーム削除
    def work_mode_frm_destroy(self):
        if self.work_mode_frm != None:
            self.work_mode_frm.destroy()
            self.work_mode_frm = None
    
    #   作業者用モードフレーム終了
    def work_mode_frm_finish(self):
        self.work_mode_frm_destroy()
        self.show_main_frm()

    #   寸法検査ログフレーム生成
    def size_log_frm_create(self):
        self.size_log_frm = tk.Frame(self.rootform,width=1920,height=1080)
        self.size_log_frm.pack()

        #   部品を生成
        buttonR1 = tk.Button(self.size_log_frm,text="戻る",font=("",40),command=self.size_log_frm_finish)
        #   部品を配置
        buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   寸法検査ログフレーム削除
    def size_log_frm_destroy(self):
        if self.size_log_frm != None:
            self.size_log_frm.destroy()
            self.size_log_frm = None
    
    #   寸法検査ログフレーム終了
    def size_log_frm_finish(self):
        self.size_log_frm_destroy()
        self.show_work_mode_frm()

    #   外観検査ログフレーム生成
    def vision_frm_create(self):
        self.vision_frm = tk.Frame(self.rootform,width=1920,height=1080)
        self.vision_frm.pack()

        #   部品を生成
        buttonR1 = tk.Button(self.vision_frm,text="戻る",font=("",40),command=self.vision_frm_finish)
        #   部品を配置
        buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   外観検査ログフレーム削除
    def vision_frm_destroy(self):
        if self.vision_frm != None:
            self.vision_frm.destroy()
            self.vision_frm = None
    
    #   外観検査ログフレーム終了
    def vision_frm_finish(self):
        self.vision_frm_destroy()
        self.show_work_mode_frm()
    
    #   カウントログフレーム生成
    def count_frm_create(self):
        if self.count_frm == None:
            self.count_frm = tk.Frame(self.rootform,width=1920,height=1080)
            self.count_frm.pack()

            #   部品を生成
            button_cr_today = tk.Button(self.count_frm,text="本日の記録",font=("",30), command=self.count_log)
            button_cr_7days = tk.Button(self.count_frm,text="七日間の記録",font=("",27), command=self.count_log_7_days)
            buttonR3 = tk.Button(self.count_frm,text="戻る",font=("",40), command=self.count_frm_finish)
            self.count_vitals = tk.Label(self.count_frm,text=self.vitals_msg,
                                        font=("",30),relief=tk.SOLID)
        
            #   部品を配置
            buttonR3.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
            button_cr_today.place(relx=0.02,rely=0.2, relwidth=0.12, relheight=0.12)
            button_cr_7days.place(relx=0.02,rely=0.34, relwidth=0.12, relheight=0.12)
            self.count_vitals.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.1)

            # self.vitals_flg = self.rootform.after(1000,self.vital_update,self.count_vitals)

    #   カウントログフレーム削除
    def count_frm_destroy(self):
        if self.count_frm != None:
            self.count_frm.destroy()
            self.count_frm = None
            self.canvas = None
    
    def count_frm_finish(self):
        self.count_frm_destroy()
        self.show_work_mode_frm()
        
    
    #   メンテナンスモードフレーム生成
    def admin_mode_frm_create(self):
        if self.admin_mode_frm == None:
            self.admin_mode_frm = tk.Frame(self.rootform,width=1920,height=1080)#bg="red"
            self.admin_mode_frm.pack()

            #   部品生成
            text1 = tk.Label(self.admin_mode_frm,text="メンテナンス",font=("",20))
            buttonM1 = tk.Button(self.admin_mode_frm,text="メンテナンス1")
            buttonM2 = tk.Button(self.admin_mode_frm,text="メンテナンス2")
            buttonM3 = tk.Button(self.admin_mode_frm,text="メンテナンス3")
            buttonM4 = tk.Button(self.admin_mode_frm,text="メンテナンス4")
            buttonM5 = tk.Button(self.admin_mode_frm,text="メンテナンス5")
            buttonM6 = tk.Button(self.admin_mode_frm,text="メンテナンス6")
            buttonR2 = tk.Button(self.admin_mode_frm,text="戻る",font=("",40),command=self.admin_mode_frm_finish)
            #   部品配置
            text1.place(relx=0, rely=0.05, relwidth=0.2, relheight=0.1)
            buttonR2.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

            

    #   メンテナンスモードフレーム削除
    def admin_mode_frm_destroy(self):
        if self.admin_mode_frm != None:
            self.admin_mode_frm.destroy()
            self.admin_mode_frm = None

    #   メンテナンスモードフレーム終了
    def admin_mode_frm_finish(self):
        self.admin_mode_frm_destroy()
        self.show_main_frm()

    #   メインフレームを表示
    def show_main_frm(self):
        #   生成していれば
        if self.main_frm != None:
            self.main_frm.pack()    #   メインフレームを表示
            self.vital_update_finish()
            self.vital_update(self.main_vitals)
        #   生成していなければ
        else:
            self.main_frm_create()  #   メインフレームを生成
    
    #   ワークフレームを表示
    def show_work_mode_frm(self):
        self.main_frm.pack_forget() #   メインフレームを非表示
        #   ワークフレームを生成していれば
        if self.work_mode_frm != None:
            self.vital_update_finish()
            self.work_mode_frm.pack()   #   ワークフレームを表示
            self.vital_update(self.work_vitals)
            if self.cansel_id != None:
                self.rootform.after_cancel(self.cansel_id)
                self.cansel_id = None
        else:
            self.vital_update_finish()
            self.work_mode_frm_create() #   ワークフレームを生成
            self.cansel_id = None
            self.tree  = None
            self.canvas = None
        self.flag_01 = 0
        self.flag_02 = 0
        self.flag_03 = 0

    def show_admin_mode_frm(self):
        self.main_frm.pack_forget()
        self.admin_mode_frm_create()

    #   外観検査フレームの表示
    def show_vision_frm(self):
        #   ワークフレームを非表示
        self.work_mode_frm.pack_forget()
        self.vision_frm_create()    #   フレームを生成
        self.flag_01 = 1    #   ﾌﾗｸﾞを設定
        self.vision_up()    #   画像を表示

    #   寸法検査フレームの表示(グラフ)
    def show_size_log_frm(self):
        #   ワークフレームを非表示
        self.work_mode_frm.pack_forget()
        self.size_log_frm_create()  #   寸法検査フレームを生成
        self.flag_02 = 1
        self.show_size_log_graph()
 
    #   寸法検査ログフレームの表示
    def show_count_frm(self):
        #   ワークフレームを非表示
        self.vital_update_finish()
        self.work_mode_frm.pack_forget()
        self.count_frm_create()  #   寸法検査ログフレームを生成
        self.vital_update(self.count_vitals)
        self.flag_03 = 1
        self.count_log()

    #   外観検査画像表示処理
    def vision_up(self):
        # dir_path = Path("D:/GitHub/Kaihatsu_G2/UI試作/真鍮_白黒画像")
        dir_path = Path("D:\\GitHub\\Kaihatsu_G2\\UI試作\\真鍮_白黒画像")
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
        w_size = int(img1.width/2.5)
        h_size = int(img1.height/2.5)
        self.ttk_img = None
        self.ttk_img=ImageTk.PhotoImage(image=img1.resize((w_size,h_size))) # Pillowで読み込んだ画像をtkinterで表示できるよう設定
        cvs=tk.Canvas(self.vision_frm,width=w_size-2,height=h_size-2,bg="red")# tkinterは標準でJPEGを表示できないため
        cvs.create_image(0,0,image=self.ttk_img,anchor=tk.NW)
        cvs.place(relx=0.1,rely=0.1,anchor=tk.NW)

        #rootform.after(1000,vision_up)#1秒ごとに処理
        print(self.flag_01)
        if(self.flag_01 == 1):
            self.cansel_id = self.rootform.after(1000,self.vision_up)    #1秒ごとに処理
 
    #   グラフを生成
    def graph(self):
        #   データベースからデータを取得
        size_list=[]
        result = self.db.table_data_get('testdb_02',"select * from DB_sizelog order by id desc limit 10")
        for i in result:
            size_list.append(i[2])
        print(size_list)
        size_show = list(reversed(size_list))   #   配列の順序を変更(反転)
        x = [1,2,3,4,5,6,7,8,9,10]
        y = size_show
        yh = [] #   上限
        yl = [] #   下限
        for i in range(0,10,1):
            yh.append(0.1)
            yl.append(-0.1)
        
        fig = plt.Figure(figsize=(10,8))
        instance = fig.subplots()

        instance.plot(x,y)
        instance.plot(x,yh)
        instance.plot(x,yl)
        print("graph_run")
        return fig

    #   グラフを表示
    def show_size_log_graph(self):
        #   グラフ表示領域を生成
        self.canvas = FigureCanvasTkAgg(self.graph(),master=self.size_log_frm)
        self.canvas.get_tk_widget().place(relx=0.1, rely=0.1)
        #   動作確認用
        ut=time.time()
        print(ut)
        if(self.flag_02 == 1):
            self.cansel_id = self.rootform.after(5000,self.show_size_log_graph)

    #   当日のカウントログ
    def count_log(self):
        #   自動更新が有効ならば
        if self.cansel_id != None:
            self.rootform.after_cancel(self.cansel_id)
        
        #   表が生成されているならば
        if self.tree != None:
            self.tree.destroy()

        if self.display_label != None:
            self.display_label.destroy()

        #   現在の表示内容を更新
        self.display_label = tk.Label(self.count_frm, text="本日の記録",font=("",32))
        self.display_label.place(relx=0.1,rely=0.02, relwidth=0.12, relheight=0.12)

        self.tree=ttk.Treeview(self.count_frm,column=('NO','good_size','bad_size','good_vision','bad_vision'),show='headings')

        style = ttk.Style()
        style.configure('Treeview.Heading',rowheight=100,font=("",50))
        style.configure('Treeview',rowheight=120,font=("",95))
        
        self.tree.column('NO',width=150,anchor='center')
        self.tree.column('good_size',width=150,anchor='center')
        self.tree.column('bad_size',width=150,anchor='center')
        self.tree.column('good_vision',width=150,anchor='center')
        self.tree.column('bad_vision',width=150,anchor='center')

        self.tree.heading('NO',text='総個数',anchor='center')
        self.tree.heading('good_size',text='寸法良',anchor='center')
        self.tree.heading('bad_size',text='寸法不良',anchor='center')
        self.tree.heading('good_vision',text='外観良',anchor='center')
        self.tree.heading('bad_vision',text='外観不良',anchor='center')

        result = self.db.table_data_get('testdb_02',"select * from db_now")
        for i in result:
            print(i)#i[0]-[5]:[0]id,[1]day,[2]good_size,[3]good_vision,[4]bad_size,[5]bad_vision

        self.tree.insert(parent='',index='end',values=(i[2]+i[4],i[2],i[4],i[3],i[5]))

        self.tree.place(width=1600,height=300,relx=0.15,rely=0.3,anchor=tk.NW)

        if(self.flag_03 == 1):
            self.cansel_id = self.rootform.after(5000,self.count_log)

    #   七日間のログ
    def count_log_7_days(self):
        #   当日のカウントログ表示の自動更新設定を解除
        if self.cansel_id != None:
            self.rootform.after_cancel(self.cansel_id)
        
        if self.tree != None:
            self.tree.destroy()
        
        if self.display_label != None:
            self.display_label.destroy()

        self.display_label = tk.Label(self.count_frm, text="七日間の記録",font=("",27))
        self.display_label.place(relx=0.02,rely=0.02, relwidth=0.12, relheight=0.12)

        #   表のクラスを生成
        self.tree=ttk.Treeview(self.count_frm,column=('days','NO','good_size','bad_size','good_vision','bad_vision'),show='headings')
        
        #   表の書式を設定
        style = ttk.Style()
        style.configure('Treeview.Heading',rowheight=100,font=("",50))
        style.configure('Treeview',rowheight=100,font=("",70)) 
        #   カラムを設定
        self.tree.column('days',width=124,anchor='center')
        self.tree.column('NO',width=140,anchor='center')
        self.tree.column('good_size',width=140,anchor='center')
        self.tree.column('bad_size',width=160,anchor='center')
        self.tree.column('good_vision',width=140,anchor='center')
        self.tree.column('bad_vision',width=160,anchor='center')
        #   ヘッダーを設定
        self.tree.heading('days',text='日付',anchor='center')
        self.tree.heading('NO',text='総個数',anchor='center')
        self.tree.heading('good_size',text='寸法良',anchor='center')
        self.tree.heading('bad_size',text='寸法不良',anchor='center')
        self.tree.heading('good_vision',text='外観良',anchor='center')
        self.tree.heading('bad_vision',text='外観不良',anchor='center')
        #   結果を取得
        result = self.db.table_data_get('testdb_02',"select * from db_countlog order by id DESC limit 7")
        #   iに結果を代入し、表に代入
        for i in result:
            print(i)#i[0]-[5]:[0]id,[1]day,[2]good_size,[3]good_vision,[4]bad_size,[5]bad_vision
            #   試作
            if type(i[1]) == str:
                day = ""
                for size in range((len(i[1]) - 5)):
                    day = day + (i[1][size + 5])
                print(day)
                self.tree.insert(parent='',index='end',values=(day,i[2]+i[4],i[2],i[4],i[3],i[5]))
        #   表を配置
        self.tree.place(width=1600,height=800,relx=0.15,rely=0.02,anchor=tk.NW)
        #   ﾌﾗｸﾞが立っていたら
        if(self.flag_03 == 1):
            self.cansel_id = self.rootform.after(5000,self.count_log_7_days)#後ろで状態監視が動いているのが時々出てくる

    #  終了処理
    def click_close(self):
        if messagebox.askokcancel("確認","終了しますか?"):
            self.rootform.destroy()

    #   メッセージ更新
    # def vitals_update(self):
    #     self.main_vitals["text"] = self.vitals_msg
    #     print("実行")
    #     self.rootform.after(1000,self.vitals_update)

    #   稼働状態メッセージを更新
    def vital_update(self, target_label):
        target_label["text"] = self.vitals_msg
        if self.vitals_msg == "非常停止中":
            target_label["bg"] = "red"
        else:
            target_label["bg"] = "white"
        print("実行")
        self.vitals_flg = self.rootform.after(1000,self.vital_update,target_label)

    #   稼働状態自動更新を終了
    def vital_update_finish(self):
        self.rootform.after_cancel(self.vitals_flg)
        print("キャンセル")
        self.vitals_flg = None
    
    #   PLCから状態の受け取り、反映場所　afterを入れてずっと動かす
    #   下記の関数は動作確認用であるため、参考程度にとどめて下さい
    def test(self):
        if self.vitals_msg == "稼働中":
            self.vitals_msg = "停止中"
        elif self.vitals_msg == "停止中":
            self.vitals_msg = "非常停止中"
        else:
            self.vitals_msg = "稼働中"
        # print(self.vitals_msg)
        self.rootform.after(5000,self.test)
    
if __name__ == "__main__":
    app = GUI()

