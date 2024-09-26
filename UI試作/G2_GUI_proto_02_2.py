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

import threading
from SerialConnection import SerialConnection as Serial
from Measurement import Meas
from PLC_commands import Commands as Com
from commands import Commands
import struct

# シリアル通信用
PORT1 = "COM6"  # PC用
PORT2 = "COM5"  # Digital用
BAUD_RATE1 = 9600  # ボーレート 9600
BAUD_RATE2 = 2400  # ボーレート 2400
TIMEOUT = 1  # タイムアウト時間

class GUI():
    #   初期化
    def __init__(self):
        self.rootform = tk.Tk()
        self.rootform.title('vaital_test')
        self.rootform.geometry("1920x1080")#900x600,1920x1080
        self.rootform.attributes('-fullscreen', True)   #   フルスクリーン
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
        self.cansel_id = None       #   カウント、サイズ、外観検査結果の画面自動更新解除用
        self.tree  = None           #   カウントログ表示に使用
        self.canvas = None          #   グラフ描画に使用
        self.display_label = None   #   カウントの表示項目掲示に使用
        self.flag_01 = 0            #   以下自動更新制御用ﾌﾗｸﾞ
        self.flag_02 = 0
        self.flag_03 = 0
        #   稼働状況関係
        self.vitals_msg = None      #   稼働状況のメッセージ
        self.error_flag = None      #   稼働状況のフラグ(error)
        self.vitals_id = None       #   自動更新のプロセスID(afterの戻り値)
        self.main_vitals = None     #   以下各画面の稼働状況表示用ラベル
        self.work_vitals = None
        self.size_vitals = None
        self.vision_vitals = None
        self.count_vitals = None
        self.admin_vitals = None
        #   外観検査
        self.ttk_img = None         #   外観検査の画像を保持
        # シリアル通信用
        self.recive1 = None
        self.send1 = None
        self.recive2 = None
        self.send2 = None
        self.send_word = None
        # self.show_main_frm()
        # self.rootform.protocol("WM_DELETE_WINDOW",self.click_close)
        # self.rootform.mainloop()
        #　パスワード
        self.password = None

    #   稼働状態メッセージを更新　　※画面遷移のたびにその画面のラベルに応じて実行させるため裏でafterがどんどん増えていく,古いものはvital_update_finish()で消す
    def vital_update(self, target_label):
        target_label["text"] = self.vitals_msg
        if self.vitals_msg == "稼働中":
            target_label["bg"] = "yellow green"
        elif self.vitals_msg == "停止中":
            target_label["bg"] = "yellow"
        else:
            target_label["bg"] = "red"
        self.vitals_id = self.rootform.after(1000,self.vital_update,target_label)
        # print("vital_flg:" + self.vitals_id)

    #   稼働状態自動更新を終了
    def vital_update_finish(self):#自動更新(after)が複数同時に立ち上がらないようにするため、画面遷移のたびに古いものを終了させる
        if self.vitals_id != None:
            self.rootform.after_cancel(self.vitals_id)
            print("キャンセル")
            self.vitals_id = None

    #   PLCから状態の受け取り、反映場所　afterを入れてずっと動かす
    #   下記の関数は動作確認用であるため、参考程度にとどめて下さい
    def vaital_test(self):

        if self.vitals_msg == "稼働中":
            self.vitals_msg = "停止中"
            #self.vitals_msg = Commands.change_command(99)#"非常停止中"
            #self.vitals_msg = "エラー01"
        else:
            self.vitals_msg = "稼働中"
        print(self.vitals_msg)
        self.id3 = self.rootform.after(5000,self.vaital_test)

    #   メインフレーム生成
    def main_frm_create(self):
        self.main_frm = tk.Frame(self.rootform, width=1920,height=1080)
        self.main_frm.pack()
        
        self.vitals_msg = "稼働中"#--------------------稼働状況のメッセージ

        #   テキストの設定
        text01 = tk.Label(self.main_frm,
                         text="検査・蓄積収納装置",
                         font=("",70))
        text02 = tk.Label(self.main_frm,
                            text="・データ閲覧",
                            anchor=tk.NW,
                            relief=tk.SOLID,
                            font=("",60))
        text03 = tk.Label(self.main_frm,
                            text="カウントログ",
                            anchor=tk.W,
                            font=("",50))
        text04 = tk.Label(self.main_frm,
                            text="寸法検査ログ",
                            anchor=tk.W,
                            font=("",50))
        text05 = tk.Label(self.main_frm,
                            text="外観検査ログ",
                            anchor=tk.W,
                            font=("",50))
        text06 = tk.Label(self.main_frm,
                            text="・メンテナンス",
                            anchor=tk.W,
                            font=("",60))
        self.main_vitals = tk.Label(self.main_frm,
                                    text=self.vitals_msg,
                                    relief=tk.SOLID,
                                    font=("",30))
        
        self.clock=tk.Label(self.main_frm,font=("",35))

        #   ボタン生成
        button1 = tk.Button(self.main_frm,
                            text="データ閲覧",
                            #style="sample.TButton",
                            font=("",50),
                            command=self.show_work_mode_frm)      #Button-ボタン
        button2 = tk.Button(self.main_frm,
                            text="メンテナンス",
                            font=("",50),
                            command=self.click_admin)#show_admin_mode_frm
        buttonf = tk.Button(self.main_frm,
                            text="終了",
                            font=("",40),
                            command=self.click_close)

        #   部品を配置
        text01.place(relx=0.22, rely=0.05, relwidth=0.4, relheight=0.1)
        text02.place(relx=0.5, rely=0.3,relwidth=0.3, relheight=0.45) #, relwidth=0.3, relheight=0.5
        text03.place(relx=0.55, rely=0.4,relwidth=0.2, relheight=0.06)
        text04.place(relx=0.55, rely=0.46,relwidth=0.2, relheight=0.06)
        text05.place(relx=0.55, rely=0.52,relwidth=0.2, relheight=0.06)
        text06.place(relx=0.501, rely=0.6,relwidth=0.25, relheight=0.1)
        self.main_vitals.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        button1.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.2)
        button2.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
        buttonf.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
        self.clock.place(relx=0.05, rely=0.05)

        self.vaital_test()
        self.recive()

    #   作業者用モードフレーム生成
    def work_mode_frm_create(self):
        self.work_mode_frm = tk.Frame(self.rootform,width=1920,height=1080)
        self.work_mode_frm.pack()

        #   部品生成
        #   テキスト
        text01 = tk.Label(self.work_mode_frm,
                         text="データ閲覧",
                         font=("",70))
        self.work_vitals = tk.Label(self.work_mode_frm,
                                    text=self.vitals_msg,
                                    font=("",30),
                                    relief=tk.SOLID)
        #   ボタン
        buttonc = tk.Button(self.work_mode_frm,
                            text="カウントログ",
                            font=("",50),
                            command=self.show_count_frm)             #c-count
        buttons = tk.Button(self.work_mode_frm,
                            text="寸法検査ログ",
                            font=("",50),
                            command=self.show_size_log_frm)             #s-size
        buttone = tk.Button(self.work_mode_frm,
                            text="外観検査ログ",
                            font=("",50),
                            command=self.show_vision_frm)       #e-exterior
        buttonR = tk.Button(self.work_mode_frm,
                            text="戻る",
                            font=("",40),
                            command=self.work_mode_frm_finish)

        #   配置
        text01.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
        self.work_vitals.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        buttonc.place(relx=0.1, rely=0.25, relwidth=0.3, relheight=0.1)
        buttons.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.1)
        buttone.place(relx=0.1, rely=0.65, relwidth=0.3, relheight=0.1)
        buttonR.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   寸法検査ログフレーム生成
    def size_log_frm_create(self):
        self.size_log_frm = tk.Frame(self.rootform,width=1920,height=1080)
        self.size_log_frm.pack()

        #   部品を生成
        buttonR1 = tk.Button(self.size_log_frm,text="戻る",font=("",40),command=self.size_log_frm_finish)
        self.size_vitals = tk.Label(self.size_log_frm,text=self.vitals_msg,
                                font=("",30),relief=tk.SOLID)
        #   部品を配置
        buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
        self.size_vitals.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)

    #   外観検査ログフレーム生成
    def vision_frm_create(self):
        self.vision_frm = tk.Frame(self.rootform,width=1920,height=1080)
        self.vision_frm.pack()

        #   部品を生成
        buttonR1 = tk.Button(self.vision_frm,text="戻る",font=("",40),command=self.vision_frm_finish)
        self.vision_vitals = tk.Label(self.vision_frm,text=self.vitals_msg,
                        font=("",30),relief=tk.SOLID)
        #   部品を配置
        buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
        self.vision_vitals.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)

    #   カウントログフレーム生成
    def count_frm_create(self):
        if self.count_vitals != None:
            self.count_vitals.destroy()
            self.count_vitals = None
        
        if self.count_frm == None:
            self.count_frm = tk.Frame(self.rootform,width=1920,height=1080)
            self.count_frm.pack()

            #   部品を生成
            button_cr_today = tk.Button(self.count_frm,text="本日の記録",font=("",30), command=self.count_log)
            button_cr_7days = tk.Button(self.count_frm,text="七日間の記録",font=("",27), command=self.count_log_7_days)
            buttonR3 = tk.Button(self.count_frm,text="戻る",font=("",40), command=self.count_frm_finish)
            self.count_vitals = tk.Label(self.count_frm,
                                         text=self.vitals_msg,
                                        font=("",30),
                                        relief=tk.SOLID)

            #   部品を配置
            buttonR3.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
            button_cr_today.place(relx=0.02,rely=0.2, relwidth=0.12, relheight=0.12)
            button_cr_7days.place(relx=0.02,rely=0.34, relwidth=0.12, relheight=0.12)
            self.count_vitals.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)

    #   メンテナンスモードフレーム生成
    def admin_mode_frm_create(self):
        if self.admin_mode_frm == None:
            self.admin_mode_frm = tk.Frame(self.rootform,width=1920,height=1080)#bg="red"
            self.admin_mode_frm.pack()

            #   部品生成
            text01 = tk.Label(self.admin_mode_frm,text="メンテナンス",font=("",55))
            buttonM1 = tk.Button(self.admin_mode_frm,text="洗浄部",font=("",30),command=lambda:self.send(1))
            buttonM2 = tk.Button(self.admin_mode_frm,text="寸法検査部",font=("",30),command=lambda:self.send(2))
            buttonM3 = tk.Button(self.admin_mode_frm,text="分別部",font=("",30),command=lambda:self.send(3))
            buttonM4 = tk.Button(self.admin_mode_frm,text="蓄積収納部",font=("",30),command=lambda:self.send(4))
            buttonM5 = tk.Button(self.admin_mode_frm,text="外観検査部",font=("",30),command=lambda:self.send(5))
            buttonM6 = tk.Button(self.admin_mode_frm,text="分別部",font=("",30),command=lambda:self.send(6))
            buttonM7 = tk.Button(self.admin_mode_frm,text="蓄積収納部",font=("",30),command=lambda:self.send(7))
            buttonR2 = tk.Button(self.admin_mode_frm,text="戻る",font=("",40),command=self.admin_mode_frm_finish)
            self.admin_vitals = tk.Label(self.admin_mode_frm,text=self.vitals_msg,
                                        font=("",30),relief=tk.SOLID)
            #   部品配置
            text01.place(relx=0.3, rely=0.05, relwidth=0.2, relheight=0.1)
            buttonM1.place(relx=0.15, rely=0.25, relwidth=0.2, relheight=0.1)
            buttonM2.place(relx=0.15, rely=0.4, relwidth=0.2, relheight=0.1)
            buttonM3.place(relx=0.15, rely=0.55, relwidth=0.2, relheight=0.1)
            buttonM4.place(relx=0.15, rely=0.7, relwidth=0.2, relheight=0.1)
            buttonM5.place(relx=0.55, rely=0.25, relwidth=0.2, relheight=0.1)
            buttonM6.place(relx=0.55, rely=0.4, relwidth=0.2, relheight=0.1)
            buttonM7.place(relx=0.55, rely=0.55, relwidth=0.2, relheight=0.1)
            buttonR2.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
            self.admin_vitals.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)

    #   パスワードフレーム生成
    def pass_frm_create(self):
        self.pass_frm = tk.Frame(self.rootform,width=1920,height=1080)
        self.pass_frm.pack()

        #   部品生成
        #   テキスト
        self.password=""
        text01 = tk.Label(self.pass_frm,
                         text="パスワード入力",
                         font=("",50))
        self.pass_in=tk.Label(self.pass_frm,text="",font=("",45),relief=tk.SOLID)

        #   ボタン
        button01 = tk.Button(self.pass_frm,text="1",font=("",50),command=self.pass_01)
        button02 = tk.Button(self.pass_frm,text="2",font=("",50),command=self.pass_02)
        button03 = tk.Button(self.pass_frm,text="3",font=("",50),command=self.pass_03)
        button04 = tk.Button(self.pass_frm,text="4",font=("",50),command=self.pass_04)
        button05 = tk.Button(self.pass_frm,text="5",font=("",50),command=self.pass_05)
        button06 = tk.Button(self.pass_frm,text="6",font=("",50),command=self.pass_06)
        button07 = tk.Button(self.pass_frm,text="7",font=("",50),command=self.pass_07)
        button08 = tk.Button(self.pass_frm,text="8",font=("",50),command=self.pass_08)
        button09 = tk.Button(self.pass_frm,text="9",font=("",50),command=self.pass_09)
        button00 = tk.Button(self.pass_frm,text="0",font=("",50),command=self.pass_00)
        button_r = tk.Button(self.pass_frm,text="Reset",font=("",30),command=self.pass_r)
        button_e = tk.Button(self.pass_frm,text="Enter",font=("",30),command=self.pass_judge)

        buttonR4 = tk.Button(self.pass_frm,text="戻る",font=("",40),command=self.pass_frm_finish)

        #   配置
        text01.place(relx=0.25, rely=0.05, relwidth=0.4, relheight=0.1)
        self.pass_in.place(relx=0.35, rely=0.25, relwidth=0.25, relheight=0.1)
        button01.place(relx=0.32, rely=0.65, relwidth=0.1, relheight=0.1)
        button02.place(relx=0.43, rely=0.65, relwidth=0.1, relheight=0.1)
        button03.place(relx=0.54, rely=0.65, relwidth=0.1, relheight=0.1)
        button04.place(relx=0.32, rely=0.54, relwidth=0.1, relheight=0.1)
        button05.place(relx=0.43, rely=0.54, relwidth=0.1, relheight=0.1)
        button06.place(relx=0.54, rely=0.54, relwidth=0.1, relheight=0.1)
        button07.place(relx=0.32, rely=0.43, relwidth=0.1, relheight=0.1)
        button08.place(relx=0.43, rely=0.43, relwidth=0.1, relheight=0.1)
        button09.place(relx=0.54, rely=0.43, relwidth=0.1, relheight=0.1)
        button00.place(relx=0.32, rely=0.76, relwidth=0.2, relheight=0.1)
        button_r.place(relx=0.65, rely=0.43, relwidth=0.1, relheight=0.2)
        button_e.place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.2)

        buttonR4.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)


    #   メインフレーム削除
    def main_frm_destroy(self):
        if self.main_frm != None:
            self.main_frm.destroy()
            self.main_frm = None

    #   作業者湯モードフレーム削除
    def work_mode_frm_destroy(self):
        if self.work_mode_frm != None:
            self.work_mode_frm.destroy()
            self.work_mode_frm = None

        #   メンテナンスモードフレーム削除
    def admin_mode_frm_destroy(self):
        if self.admin_mode_frm != None:
            self.admin_mode_frm.destroy()
            self.admin_mode_frm = None

        #   パスワードフレーム削除
    def pass_frm_destroy(self):
        if self.pass_frm != None:
            self.pass_frm.destroy()
            self.pass_frm = None
    
        #   寸法検査ログフレーム削除
    def size_log_frm_destroy(self):
        if self.size_log_frm != None:
            self.size_log_frm.destroy()
            self.size_log_frm = None

    #   外観検査ログフレーム削除
    def vision_frm_destroy(self):
        if self.vision_frm != None:
            self.vision_frm.destroy()
            self.vision_frm = None

        #   カウントログフレーム削除
    def count_frm_destroy(self):
        if self.count_frm != None:
            self.count_frm.destroy()
            self.count_frm = None
            self.canvas = None

    #   外観検査画像表示処理
    def vision_up(self):
        dir_path = Path("D:/GitHub/Kaihatsu_G2/UI試作/真鍮_白黒画像")
        #dir_path = Path("D:/kaihatu/test/UI/img_file")
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
        #img1=Image.open("D:/kaihatu/test/UI/img_file/"f"/{list_date_new}.jpg")
        w_size = int(img1.width/2.5)
        h_size = int(img1.height/2.5)
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
        result = self.db.table_data_get('testdb_02',"select * from DB_sizelog order by id desc limit 30")
        for i in result:
            size_list.append(i[2])
        print(size_list)
        size_show = list(reversed(size_list))   #   配列の順序を変更(反転)
        x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
        y = size_show
        yh = [] #   上限
        yl = [] #   下限
        for i in range(0,30,1):
            yh.append(0.1)
            yl.append(-0.1)
        
        fig,ax = plt.subplots(figsize=(10,8))

        # フォントの設定
        plt.rcParams['font.family'] = 'HGMaruGothicMPRO'
        plt.rcParams['font.size'] = 14
        plt.rcParams['axes.titlesize'] = 24
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['legend.fontsize'] = 12

        # グラフの設定を最適化
        ax.clear()
        ax.plot(x, y, label='測定値')
        ax.plot(x, yh, label='上限')
        ax.plot(x, yl, label='下限')

        ax.set_xlabel('直近30個')
        ax.set_ylabel('差異')
        ax.set_title('寸法測定ログ')

        ax.legend(loc='upper right')

        # レイアウトを調整して、軸ラベルやタイトルが切れないようにする
        fig.tight_layout()
        
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
        self.display_label = tk.Label(self.count_frm,
                                        text="本日の記録",
                                        font=("",45))
        self.display_label.place(relx=0.1,rely=0.04)

        self.tree=ttk.Treeview(self.count_frm,column=('NO','good_size','bad_size','good_vision','bad_vision'),show='headings')

        style = ttk.Style()
        style.configure('Treeview.Heading',rowheight=100,font=("",50))
        style.configure('Treeview',rowheight=160,font=("",95))
        
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

        self.tree.place(width=1600,height=260,relx=0.15,rely=0.17,anchor=tk.NW)

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

        self.display_label = tk.Label(self.count_frm, text="七日間の記録",font=("",45))
        self.display_label.place(relx=0.1,rely=0.04)

        #   表のクラスを生成
        self.tree=ttk.Treeview(self.count_frm,column=('days','NO','good_size','bad_size','good_vision','bad_vision'),show='headings')
        
        #   表の書式を設定
        style = ttk.Style()
        style.configure('Treeview.Heading',rowheight=40,font=("",40))
        style.configure('Treeview',rowheight=85,font=("",55))
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
            print(i)    #i[0]-[5]:[0]id,[1]day,[2]good_size,[3]good_vision,[4]bad_size,[5]bad_vision
            #   試作
            if type(i[1]) == str:
                day = ""
                for size in range((len(i[1]) - 5)):
                    day = day + (i[1][size + 5])
                print(day)
                self.tree.insert(parent='',index='end',values=(day,i[2]+i[4],i[2],i[4],i[3],i[5]))
        #   表を配置
        self.tree.place(width=1600,height=690,relx=0.15,rely=0.17,anchor=tk.NW)
        #   ﾌﾗｸﾞが立っていたら
        if(self.flag_03 == 1):
            self.cansel_id = self.rootform.after(5000,self.count_log_7_days)#後ろで状態監視が動いているのが時々出てくる

    #  終了処理
    def click_close(self):
        if messagebox.askokcancel("確認","終了しますか?"):
            self.rootform.after_cancel(self.id1)
            self.clock.after_cancel(self.id2)
            self.rootform.after_cancel(self.id3)
            self.vital_update_finish()
            self.rootform.destroy()

    #  パスワード入力画面遷移
    def click_admin(self):
        if self.vitals_msg != "停止中":
            messagebox.showwarning("showwarning", "装置が安全な状態で再試行してください。")
        else:
            #self.show_admin_mode_frm()
            self.show_pass_frm()
    #時刻表示
    def tick(self):
        now=time.strftime("%H:%M:%S")
        self.clock.config(text=now)
        self.id2=self.clock.after(1000,self.tick)
    
    #パスワード入力
    def pass_01(self):
        self.password += "1"
        self.pass_in.config(text=self.password)
    def pass_02(self):
        self.password += "2"
        self.pass_in.config(text=self.password)
    def pass_03(self):
        self.password += "3"
        self.pass_in.config(text=self.password)
    def pass_04(self):
        self.password += "4"
        self.pass_in.config(text=self.password)
    def pass_05(self):
        self.password += "5"
        self.pass_in.config(text=self.password)
    def pass_06(self):
        self.password += "6"
        self.pass_in.config(text=self.password)
    def pass_07(self):
        self.password += "7"
        self.pass_in.config(text=self.password)
    def pass_08(self):
        self.password += "8"
        self.pass_in.config(text=self.password)
    def pass_09(self):
        self.password += "9"
        self.pass_in.config(text=self.password)
    def pass_00(self):
        self.password += "0"
        self.pass_in.config(text=self.password)
    #入力内容リセット
    def pass_r(self):
        self.password = ""
        self.pass_in.config(text=self.password)
    #パスワード判定
    def pass_judge(self):
        if self.password=="2024":
            self.show_admin_mode_frm()
        else:
            messagebox.showwarning("warning", "パスワードが間違っています。")

    #   メッセージ更新
    # def vitals_update(self):
    #     self.main_vitals["text"] = self.vitals_msg
    #     print("実行")
    #     self.rootform.after(1000,self.vitals_update)

    #   メインフレームを表示
    def show_main_frm(self):
        #   生成していれば
        if self.main_frm != None:
            self.main_frm.pack()    #   メインフレームを表示
        #   生成していなければ
        else:
            self.main_frm_create()  #   メインフレームを生成
        #   稼働状況更新
        self.vital_update_finish()
        self.vital_update(self.main_vitals)
    
    #   ワークフレームを表示
    def show_work_mode_frm(self):
        #   ワークフレームを生成していれば
        if self.work_mode_frm != None:
            if self.cansel_id != None:
                self.rootform.after_cancel(self.cansel_id)
                self.cansel_id = None
            self.work_mode_frm.pack()   #   ワークフレームを表示
        else:
            self.main_frm.pack_forget() #   メインフレームを非表示
            self.work_mode_frm_create() #   ワークフレームを生成
        #   自動更新
        self.vital_update_finish()
        self.vital_update(self.work_vitals)
        #   初期化
        self.cansel_id = None
        self.tree  = None
        self.canvas = None
        self.flag_01 = 0
        self.flag_02 = 0
        self.flag_03 = 0

    #   メンテナンスフレームを表示
    def show_admin_mode_frm(self):
        self.pass_frm.pack_forget()
        self.admin_mode_frm_create()
        self.vital_update_finish()
        self.vital_update(self.admin_vitals)

    #   パスワードフレームを表示
    def show_pass_frm(self):
        self.main_frm.pack_forget()
        self.pass_frm_create()

    #   外観検査フレームの表示
    def show_vision_frm(self):
        self.work_mode_frm.pack_forget()#   ワークフレームを非表示
        self.vision_frm_create()    #   フレームを生成
        self.vital_update_finish()
        self.vital_update(self.vision_vitals)
        self.flag_01 = 1    #   ﾌﾗｸﾞを設定
        self.vision_up()    #   画像を表示

    #   寸法検査フレームの表示(グラフ)
    def show_size_log_frm(self):
        self.work_mode_frm.pack_forget()#   ワークフレームを非表示
        self.size_log_frm_create()  #   寸法検査フレームを生成
        self.vital_update_finish()
        self.vital_update(self.size_vitals)
        self.flag_02 = 1
        self.show_size_log_graph()
 
    #   寸法検査ログフレームの表示
    def show_count_frm(self):
        self.work_mode_frm.pack_forget()#   ワークフレームを非表示
        self.count_frm_create()  #   寸法検査ログフレームを生成
        self.vital_update_finish()
        self.vital_update(self.count_vitals)
        self.flag_03 = 1
        self.count_log()

        #   作業者用モードフレーム終了
    def work_mode_frm_finish(self):
        self.work_mode_frm_destroy()
        self.show_main_frm()
    
    #   寸法検査ログフレーム終了
    def size_log_frm_finish(self):
        self.size_log_frm_destroy()
        self.show_work_mode_frm()
    
    #   外観検査ログフレーム終了
    def vision_frm_finish(self):
        self.vision_frm_destroy()
        self.show_work_mode_frm()
    
    #   カウントログフレーム終了
    def count_frm_finish(self):
        self.count_frm_destroy()
        self.show_work_mode_frm()

    #   メンテナンスモードフレーム終了
    def admin_mode_frm_finish(self):
        self.admin_mode_frm_destroy()
        self.show_main_frm()

    #   パスワードフレーム終了
    def pass_frm_finish(self):
        self.pass_frm_destroy()
        self.show_main_frm()

    #   アプリスタート
    def start(self):
        self.show_main_frm()
        self.rootform.protocol("WM_DELETE_WINDOW",self.click_close)
        self.tick()
        self.rootform.mainloop()

    # シリアル通信のデータ受信
    def recive(self):
        data1 = serial_conn1.get_receive_word()
        if data1:
            # 受信データを変数に格納→表示
            self.recive1 = struct.unpack('>B',data1)[0]
            print(f"PLCから受信:{self.recive1}")
            data1 = ""
            self.case_chack()
            self.send()
        self.id1 = self.rootform.after(1000,self.recive)  # 0.5秒ごとに更新        
    
    def send(self, send = None):
        if self.recive1 == b"s":    # インジケータ実行コマンド
            serial_conn2.set_send_word(b"s")    # 送信
            self.recive2 = serial_conn2.get_receive_word()
            print(f"インジケータから受信:{self.recive2}")
            self.recive1 = None
        elif self.recive1:
            self.send_word = com.change_command(self.recive1)
            if self.send_word:
                serial_conn1.set_send_word(self.send_word)
                self.send_word = None
            self.recive1 = None
        elif send and self.error_flag != True:
            serial_conn1.set_send_word(send)
    
    def case_chack(self):
        if 0 <= self.recive1 and 100 >= self.recive1:
            self.error()
        elif 100 < self.recive1 and 150 >= self.recive1:
            # 動作開始命令用処理
            pass
        elif 150 < self.recive1 and 200 >= self.recive1:
            # 動作終了伝達用処理
            pass
    
    def error(self):
        # ラベルの更新
        self.vitals_msg = msg.change_command(self.recive1)
        # errorフラグON
        self.error_flag = True
    
if __name__ == "__main__":
    # デジタルインジケータのクラス作成
    meas = Meas()

    com = Com()

    msg = Commands()

    # シリアル通信のクラス作成
    serial_conn1 = Serial(PORT1,BAUD_RATE1,TIMEOUT)
    serial_conn2 = Serial(PORT2,BAUD_RATE2,TIMEOUT)

    # PLCに接続
    serial_conn1.connect()
    # デジタルインジケータに接続
    serial_conn2.connect()

    # シリアルポートが開かれている
    if serial_conn1.is_open and serial_conn2.is_open:
        # PLC通信用スレッド
        receive_plc = threading.Thread(target=serial_conn1.receive_data)
        receive_plc.start()
        send_plc = threading.Thread(target=serial_conn1.send_data)
        send_plc.start()

        # デジタルインジケータ用スレッド
        receive_digital = threading.Thread(target=serial_conn2.receive_data)
        receive_digital.start()
        send_digital = threading.Thread(target=serial_conn2.send_data)
        send_digital.start()
        time.sleep(3)

    # if serial_conn1.is_open:
    #     # PLC通信用スレッド
    #     receive_plc = threading.Thread(target=serial_conn1.receive_data)
    #     receive_plc.start()
    #     send_plc = threading.Thread(target=serial_conn1.send_data)
    #     send_plc.start()
    
    app = GUI()
    app.start()

    # シリアル通信終了処理
    serial_conn1.shutdown_flag = True
    serial_conn2.shutdown_flag = True

    if serial_conn1.is_open:
        serial_conn1.close()
    if serial_conn2.is_open:
        serial_conn2.close()

    print("プログラムを終了します.")