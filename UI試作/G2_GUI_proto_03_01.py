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
import time

import threading
from SerialConnection import SerialConnection as Serial
from Measurement import Meas
from PLC_commands import Commands as Com
from commands import Commands
import struct

#   シリアル通信用
PORT1 = "COM6"  # PC用
PORT2 = "COM5"  # Digital用
BAUD_RATE1 = 9600  # ボーレート 9600
BAUD_RATE2 = 2400  # ボーレート 2400
TIMEOUT = 1  # タイムアウト時間
FILE_PASS = "D:/Kaihatsu/VScode/GUI/image"

class GUI():
    #   初期化
    def __init__(self):
        #   ルートフレームを生成
        self.root_frm = tki.Tk()
        self.root_frm.title('vaital_test')
        self.root_frm.geometry("1920x1080")#900x600,1920x1080
        self.root_frm.attributes('-fullscreen', True)   #   フルスクリーン
        #   各フレームを初期化
        self.main_frm = None                        #   メインページ
        self.data_list_frm = None                   #   データ一覧
        self.pass_frm = None                       #   パスワード
        self.maintenance_frm = None                 #   メンテナンス
        self.judgment_result_frm = None             #   良否判定
        self.size_graph_frm = None                  #   寸法測定結果
        self.visual_inspection_frm = None           #   外観検査
        #   パスワード入力フォーム用
        self.input_pass =  None
        #   自動更新用
        self.tree = None            #   良否判定を表示する際に使用
        self.fig = None             #   グラフを保持するために使用
        self.canvas = None          #   グラフを描画するために必要
        self.label_item_name = None #   良否判定の表示項目を表示する際に使用
        self.cvs = None             #   画像を描画する際に使用
        #   稼働状況表示用
        self.operational_status = None  #   稼働状況を保持
        self.error_flag = None          #   稼働状況のフラグ
        self.status_label = None        #   稼働状況表示用ラベル
        #   外観検査
        self.visual_img = None          #   外観検査の画像を保持
        #   シリアル通信用
        self.recv_plc_msg = None        #   PLCからのメッセージ
        self.send_plc_msg = None        #   PLCへのメッセージ
        self.recv_indicator_msg = None  #   インジケータからのメッセージ
        self.send_indicator_msg = None  #   インジケータへのメッセージ
        self.send_word = None           #   送信するデータを格納
        #   アフター解除用
        self.after_cancel_id = None #   良否判定、寸法測定、外観検査の自動更新解除に使用
        self.after_rcv_id = None    #   繰り返し受信解除に使用
        self.after_update_id = None #   稼働状況の自動更新解除に使用
        self.after_test_id = None   #   デバック用
        #   フレーム切替用
        self.switching_main = "0"
        self.switching_data = "1"
        self.switching_maintenance = "2"
        self.switching_judge = "3"
        self.switching_meas = "4"
        self.switching_visual = "5"
        self.switching_pass = "6"
        #   データベース用
        self.db_com=DMC.DbCommunication()

    #   稼働状況の表示ラベルを更新する
    def _update_status_label(self,frm:Frame):
        update_label = frm.nametowidget("status")
        #   試験用
        if self.operational_status.get() == "稼働中":
            self.operational_status.set("停止中")   
            update_label.config(bg="yellow")
        elif self.operational_status.get() == "停止中":
            self.operational_status.set("緊急停止")
            update_label.config(bg="red")
        else:
            self.operational_status.set("稼働中")
            update_label.config(bg="yellow green")
        self.after_update_id = self.root_frm.after(1000,self._update_status_label, frm)

    #   稼働状況自動更新を停止する
    def _finish_status_update_label(self):
        if self.after_update_id != None:
            self.root_frm.after_cancel(self.after_update_id)
            self.after_update_id = None
    
    #   稼働状況自動更新を開始する
    def _start_update_status_label(self,frm:Frame):
        self._finish_status_update_label()
        self._update_status_label(frm)
    
    #   メインフレームを生成
    def _create_main_frm(self):
        self.main_frm = tki.Frame(self.root_frm, width=1920,height=1080)
        self.main_frm.pack()
        if self.operational_status == None:
            self.operational_status = tki.StringVar()
        #   テキストの設定
        label_title = tki.Label(self.main_frm,
                               text="検査・蓄積収納装置",
                               font=("",70))        
        label_data_list = tki.Label(self.main_frm,
                                    text="・データ一覧",
                                    anchor=tki.NW,
                                    relief=tki.SOLID,
                                    font=("",60))
        label_judgment = tki.Label(self.main_frm,
                                    text="良否判定",
                                    anchor=tki.W,
                                    font=("",50))
        label_graph = tki.Label(self.main_frm,
                                text="寸法検査",
                                anchor=tki.W,
                                font=("",50))
        label_visual = tki.Label(self.main_frm,
                                text="外観検査",
                                anchor=tki.W,
                                font=("",50))
        label_maintenance = tki.Label(self.main_frm,
                                      text="メンテナンス",
                                      anchor=tki.W,
                                      font=("",50))
        label_status = tki.Label(self.main_frm,
                                 textvariable=self.operational_status,
                                 relief=tki.SOLID,
                                 name="status",
                                 font=("",30))
        
        #   ボタンの生成
        button_data_list = tki.Button(self.main_frm,
                                      text="データ一覧",
                                      font=("",50),
                                      command=lambda:self._show_frm(self.switching_data))
        button_maintenance = tki.Button(self.main_frm,
                                        text="メンテナンス",
                                        font=("",50),
                                        command=lambda:self._show_frm(self.switching_pass))
        button_finish = tki.Button(self.main_frm,
                                   text="終了",
                                   font=("",40),
                                   command=self._click_close)
        
        #   部品を配置
        label_title.place(relx=0.22, rely=0.05, relwidth=0.4, relheight=0.1)
        label_data_list.place(relx=0.5, rely=0.3,relwidth=0.3, relheight=0.45) #, relwidth=0.3, relheight=0.5
        label_judgment.place(relx=0.55, rely=0.4,relwidth=0.2, relheight=0.06)
        label_graph.place(relx=0.55, rely=0.46,relwidth=0.2, relheight=0.06)
        label_visual.place(relx=0.55, rely=0.52,relwidth=0.2, relheight=0.06)
        label_maintenance.place(relx=0.501, rely=0.6,relwidth=0.25, relheight=0.1)
        label_status.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        button_data_list.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.2)
        button_maintenance.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
        button_finish.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
    
    #   データ一覧フレームを生成
    def _create_data_list_frm(self):
        self.data_list_frm = tki.Frame(self.root_frm,width=1920,height=1080)
        self.data_list_frm.pack()

        #   テキストの設定
        label_title = tki.Label(self.data_list_frm,
                                text="データ閲覧",
                                font=("",70))
        label_status = tki.Label(self.data_list_frm,
                                 textvariable=self.operational_status,
                                 relief=tki.SOLID,
                                 name="status",
                                 font=("",30))
        
        button_judgment = tki.Button(self.data_list_frm,
                                     text="良否判定",
                                     font=("",50),
                                     command=lambda:self._show_frm(self.switching_judge))
        button_graph = tki.Button(self.data_list_frm,
                                  text="寸法検査",
                                  font=("",50),
                                  command=lambda:self._show_frm(self.switching_meas))
        button_visual = tki.Button(self.data_list_frm,
                                   text="外観検査",
                                   font=('',50),
                                   command=lambda:self._show_frm(self.switching_visual))
        button_back = tki.Button(self.data_list_frm,
                                 text="戻る",
                                 font=("",50),
                                 command=self._return_main_frm)
 
        #   配置
        label_title.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
        label_status.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        button_judgment.place(relx=0.1, rely=0.25, relwidth=0.3, relheight=0.1)
        button_graph.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.1)
        button_visual.place(relx=0.1, rely=0.65, relwidth=0.3, relheight=0.1)
        button_back.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   メンテナンスフレームを生成
    def _create_maintenance_frm(self):
        self.maintenance_frm = tki.Frame(self.root_frm,width=1920,height=1080)
        self.maintenance_frm.pack()

        #   ラベル生成
        label_title = tki.Label(self.maintenance_frm,
                                 text="メンテナンス",
                                 font=("",20))
        label_status = tki.Label(self.maintenance_frm,
                                 textvariable=self.operational_status,
                                 relief=tki.SOLID,
                                 name="status",
                                 font=("",30))
        #   ボタン生成
        button_back = tki.Button(self.maintenance_frm,
                                 text="戻る",
                                 font=("",40),
                                 command=self._return_main_frm)
        
        #   配置
        label_title.place(relx=0, rely=0.05, relwidth=0.2, relheight=0.1)
        label_status.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        button_back.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   良否判定結果表示フレームを生成
    def _create_judgment_result_frm(self):
        self.judgment_result_frm = tki.Frame(self.root_frm,width=1920,height=1080)
        self.judgment_result_frm.pack()

        #   ラベル生成
        label_status = tki.Label(self.judgment_result_frm,
                                 textvariable=self.operational_status,
                                 relief=tki.SOLID,
                                 name="status",
                                 font=("",30))
        self.label_item_name = tki.Label(self.judgment_result_frm,
                                        text="本日の記録",
                                        font=("",45))
        
        #   ボタン生成
        button_today = tki.Button(self.judgment_result_frm,
                                  text="本日の記録",
                                  font=("",30),
                                  command=self._create_result_today)
        button_seven_days = tki.Button(self.judgment_result_frm,
                                  text="七日間の記録",
                                  font=("",27),
                                  command=self._create_result_seven_days)
        button_back = tki.Button(self.judgment_result_frm,
                                  text="戻る",
                                  font=("",40),
                                  command=self._return_data_list_frm)
        
        #   配置
        label_status.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        self.label_item_name.place(relx=0.1,rely=0.04)
        button_today.place(relx=0.02,rely=0.2, relwidth=0.12, relheight=0.12)
        button_seven_days.place(relx=0.02,rely=0.34, relwidth=0.12, relheight=0.12)
        button_back.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   寸法測定フレームを生成
    def _create_size_graph_frm(self):
        self.size_graph_frm = tki.Frame(self.root_frm,width=1920,height=1080)
        self.size_graph_frm.pack()

        #   ラベルとボタンを生成
        label_status = tki.Label(self.size_graph_frm,
                                 textvariable=self.operational_status,
                                 relief=tki.SOLID,
                                 name="status",
                                 font=("",30))
        button_back = tki.Button(self.size_graph_frm,
                                 text="戻る",
                                 font=("",40),
                                 command=self._return_data_list_frm)
        
        #   配置
        label_status.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        button_back.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   外観検査フレームを生成
    def _create_visual_inspection_frm(self):
        self.visual_inspection_frm = tki.Frame(self.root_frm,width=1920,height=1080)
        self.visual_inspection_frm.pack()

        #   部品を生成
        #   ラベルとボタンを生成
        label_status = tki.Label(self.visual_inspection_frm,
                                 textvariable=self.operational_status,
                                 relief=tki.SOLID,
                                 name="status",
                                 font=("",30))
        button_back = tki.Button(self.visual_inspection_frm,
                                 text="戻る",
                                 font=("",40),
                                 command=self._return_data_list_frm)
        #   部品を配置
        label_status.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        button_back.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   パスワードフレーム生成
    def _create_pass_frm(self):
        self.pass_frm = tki.Frame(self.root_frm,width=1920,height=1080)
        self.pass_frm.pack()

        if self.input_pass == None:
            self.input_pass = tki.StringVar()
            self.input_pass.set("")
            print(self.input_pass.get())

        #   テキスト生成
        label_title = tki.Label(self.pass_frm,
                                text="パスワード入力",
                                font=("",50))
        label_pass = tki.Label(self.pass_frm,
                               textvariable=self.input_pass,
                               font=("",45),
                               name="pass",
                               relief=tki.SOLID)
        
        #   ボタン
        button_01 = tki.Button(self.pass_frm,
                               text="1",
                               font=("",50),
                               command=lambda:self.set_pass("1"))
        print("01:",self.input_pass.get(), "x")
        button_02 = tki.Button(self.pass_frm,
                               text="2",
                               font=("",50),
                               command=lambda:self.set_pass("2"))
        print("02:",self.input_pass.get(), "x")
        button_03 = tki.Button(self.pass_frm,
                               text="3",
                               font=("",50),
                               command=lambda:self.set_pass("3"))
        print("03:",self.input_pass.get(), "x")
        button_04 = tki.Button(self.pass_frm,
                               text="4",
                               font=("",50),
                               command=lambda:self.set_pass("4"))
        print("04:",self.input_pass.get(), "x")
        button_05 = tki.Button(self.pass_frm,
                               text="5",
                               font=("",50),
                               command=lambda:self.set_pass("5"))
        print("05:",self.input_pass.get(), "x") 
        button_06 = tki.Button(self.pass_frm,
                               text="6",
                               font=("",50),
                               command=lambda:self.set_pass("6"))
        print("06:",self.input_pass.get(), "x")
        button_07 = tki.Button(self.pass_frm,
                               text="7",
                               font=("",50),
                               command=lambda:self.set_pass("7"))
        print("07:",self.input_pass.get(), "x")
        button_08 = tki.Button(self.pass_frm,
                               text="8",
                               font=("",50),
                               command=lambda:self.set_pass("8"))
        print("08: ",self.input_pass.get(), "x")
        button_09 = tki.Button(self.pass_frm,
                               text="9",
                               font=("",50),
                               command=lambda:self.set_pass("9"))
        print("09:",self.input_pass.get(), "x")
        button_00 = tki.Button(self.pass_frm,text="0",
                               font=("",50),
                               command=lambda:self.set_pass("0"))
        print("00:",self.input_pass.get(), "x")
        button_resrt = tki.Button(self.pass_frm,
                                 text="Reset",
                                 font=("",30),
                                 command=lambda:self.set_pass("r"))
        print("r:",self.input_pass.get())
        button_enter = tki.Button(self.pass_frm,
                                  text="Enter",
                                  font=("",30),
                                  command=self.judge_pass)
        button_back = tki.Button(self.pass_frm,
                              text="戻る",
                              font=("",40),
                              command=self._return_main_frm)
        
        #   配置
        label_title.place(relx=0.25, rely=0.05, relwidth=0.4, relheight=0.1)
        label_pass.place(relx=0.35, rely=0.25, relwidth=0.25, relheight=0.1)
        button_01.place(relx=0.32, rely=0.65, relwidth=0.1, relheight=0.1)
        button_02.place(relx=0.43, rely=0.65, relwidth=0.1, relheight=0.1)
        button_03.place(relx=0.54, rely=0.65, relwidth=0.1, relheight=0.1)
        button_04.place(relx=0.32, rely=0.54, relwidth=0.1, relheight=0.1)
        button_05.place(relx=0.43, rely=0.54, relwidth=0.1, relheight=0.1)
        button_06.place(relx=0.54, rely=0.54, relwidth=0.1, relheight=0.1)
        button_07.place(relx=0.32, rely=0.43, relwidth=0.1, relheight=0.1)
        button_08.place(relx=0.43, rely=0.43, relwidth=0.1, relheight=0.1)
        button_09.place(relx=0.54, rely=0.43, relwidth=0.1, relheight=0.1)
        button_00.place(relx=0.32, rely=0.76, relwidth=0.2, relheight=0.1)
        button_resrt.place(relx=0.65, rely=0.43, relwidth=0.1, relheight=0.2)
        button_enter.place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.2)
        button_back.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    #   フレーム削除
    def _destroy_frm(self):
        if self.visual_inspection_frm:              #   フレームが存在していれば
            self.visual_inspection_frm.destroy()    #   フレームを破棄
            self.visual_inspection_frm = None       #   Noneを代入
        elif self.size_graph_frm:                   #   以下は対象フレームを変えて上記の処理を行っている
            self.size_graph_frm.destroy()
            self.size_graph_frm = None
        elif self.judgment_result_frm:
            self.judgment_result_frm.destroy()
            self.judgment_result_frm = None
        elif self.data_list_frm:
            self.data_list_frm.destroy()
            self.data_list_frm = None
        elif self.pass_frm:
            self.pass_frm.destroy()
            self.pass_frm = None
        elif self.maintenance_frm:
            self.maintenance_frm.destroy()
            self.maintenance_frm = None
        elif self.main_frm:
            self.main_frm.destroy()
            self.main_frm = None
    
    #   外観検査画像表示処理(繰り返す)
    def _update_visual_img(self):
        if self.cvs:
            self.cvs.destroy()

        #   画像を取得
        path_dir = Path(FILE_PASS)
        image_files = list(path_dir.glob("*.jpg"))
        #   日付を抽出
        list_date = []
        for i in range(len(image_files)):
            file_name,ext = os.path.splitext(image_files[i].name)
            list_date.append(file_name)
        #   新しい順にソート
        list_date_sort = sorted(list_date, reverse=True)
        list_new_date = list_date_sort[0]
        #   表示画像を読み込み
        display_image = Image.open(FILE_PASS + f"/{list_new_date}.jpg")
        print(FILE_PASS + f"/{list_new_date}.jpg")
        size_width = int(display_image.width/2.5)
        size_height = int(display_image.height/2.5)
        self.visual_img = ImageTk.PhotoImage(image=display_image.resize((size_width,size_height)))
        #   描画領域を生成
        self.cvs=tki.Canvas(self.visual_inspection_frm,
                       width=size_width-2,
                       height=size_height-2,
                       bg="red")
        self.cvs.create_image(0,0,
                         image=self.visual_img,
                         anchor=tki.NW)
        #   描画
        self.cvs.place(relx=0.1,rely=0.1,anchor=tki.NW)
        #   自動更新
        self.after_cancel_id =self.root_frm.after(1000,self._update_visual_img)
    
    #   グラフを生成
    def _create_graph(self):
        #   データベースからデータを取得
        db_result = self.db_com.table_data_get('testdb_02',"select * from DB_sizelog order by id desc limit 20")
        list_size = [i[2] for i in db_result]
        #   グラフ生成に使用するデータを用意
        show_size = list(reversed(list_size))
        x_valuses = [i for i in range(1,21)]
        y_valuses = list(reversed(list_size))
        upper_limits = [0.1] * 20
        lower_limits = [-0.1] * 20

        #   グラフを描画していなければ
        if self.fig == None:
            self.fig,self.ax = plt.subplots(figsize=(10,8))
        
        # フォントの設定
        plt.rcParams['font.family'] = 'HGMaruGothicMPRO'
        plt.rcParams['font.size'] = 14
        plt.rcParams['axes.titlesize'] = 24
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['legend.fontsize'] = 12

        # グラフの設定を最適化
        self.ax.clear()
        self.ax.plot(x_valuses, y_valuses, label='測定値')
        self.ax.plot(x_valuses, upper_limits, label='上限')
        self.ax.plot(x_valuses, lower_limits, label='下限')

        self.ax.set_xlabel('直近10個')
        self.ax.set_ylabel('差異')
        self.ax.set_title('寸法測定結果')

        self.ax.legend(loc='upper right')
        self.fig.tight_layout()

    #   グラフを表示
    def _show_graph(self):
        #   グラフを生成、更新
        self._create_graph()
        #   グラフの表示領域を生成
        self.canvas = FigureCanvasTkAgg(self.fig,master=self.size_graph_frm)
        self.canvas.get_tk_widget().place(relx=0.1,rely=0.1)
        self.after_cancel_id = self.root_frm.after(5000,self._show_graph)

    #   当日の良否判定
    def _create_result_today(self):
        if self.label_item_name.cget("text") != "本日の記録":
            self.root_frm.after_cancel(self.after_cancel_id)
            self.label_item_name["text"] = "本日の記録"
        if self.tree:
            self.tree.destroy()
        
        self.tree=ttk.Treeview(self.judgment_result_frm,column=('NO','good_size','bad_size','good_vision','bad_vision'),show='headings')
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

        result = self.db_com.table_data_get('testdb_02',"select * from db_now")
        for i in result:
            self.tree.insert(parent='',index='end',values=(i[2]+i[4],i[2],i[4],i[3],i[5]))

        self.tree.place(width=1600,height=260,relx=0.15,rely=0.17,anchor=tki.NW)
        self.after_cancel_id = self.root_frm.after(5000,self._create_result_today)

    #   七日間の良否判定
    def _create_result_seven_days(self):
        if self.label_item_name.cget("text") == "本日の記録":
            self.root_frm.after_cancel(self.after_cancel_id)
            self.label_item_name["text"] = "七日間の記録"
        if self.tree:
            self.tree.destroy()
        
        #  表のクラスを生成
        self.tree=ttk.Treeview(self.judgment_result_frm,
                                column=('days','NO','good_size','bad_size','good_vision','bad_vision'),
                                show='headings')
        
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
        result = self.db_com.table_data_get('testdb_02',"select * from db_countlog order by id DESC limit 7")
        if result:
            #   iに結果を代入し、表に代入
            for i in result:
                #   日付を抽出する関数
                if type(i[1]) == str:
                    day = ""
                    for size in range((len(i[1]) - 5)):
                        day = day + (i[1][size + 5])
                    self.tree.insert(parent='',index='end',values=(day,i[2]+i[4],i[2],i[4],i[3],i[5]))
            #   表を配置
            self.tree.place(width=1600,height=690,relx=0.15,rely=0.17,anchor=tki.NW)

    #   パスワード入力
    def set_pass(self, cmd):
        str_pass = self.input_pass.get()
        if cmd == "0":
            str_pass += "0"    
        elif cmd == "1":
            str_pass += "1"
        elif cmd == "2":
            str_pass += "2"
        elif cmd == "3":
            str_pass += "3"
        elif cmd == "4":
            str_pass += "4"
        elif cmd == "5":
            str_pass += "5"
        elif cmd == "6":
            str_pass += "6"
        elif cmd == "7":
            str_pass += "7"
        elif cmd == "8":
            str_pass += "8"
        elif cmd == "9":
            str_pass += "9"
        elif cmd == "r":
            str_pass = ""
        print(str_pass)
        self.input_pass.set(str_pass)

    #   パスワード判定
    def judge_pass(self):
        if self.input_pass.get() == "2024":
            self._show_meintenance_frm()
        else:
             messagebox.showwarning("warning", "パスワードが間違っています。")

    #   終了処理        
    def _click_close(self):
        if messagebox.askokcancel("確認","終了しますか?"):
            self._finish_status_update_label()
            # self.root_frm.after_cancel(self.after_rcv_id)
            self.root_frm.destroy()

    #   フレームを表示
    def _show_frm(self, switching_frm):
        if switching_frm == self.switching_main:
            self._show_main_frm()
        if switching_frm == self.switching_data:
            self._show_data_list_frm()
        if switching_frm == self.switching_maintenance:
            self._show_meintenance_frm()
        if switching_frm == self.switching_pass:
            self._show_pass_frm()
        if switching_frm == self.switching_judge:
            self._show_judgemnt_result_frm()
        if switching_frm == self.switching_meas:
            self._show_size_graph_frm()
        if switching_frm == self.switching_visual:
            self._show_visul_inspection_frm()
    
    #   メインフレームを表示
    def _show_main_frm(self):
        if self.main_frm:   #   生成していれば
            self.main_frm.pack()    #   メインフレームを表示
        else:   #   生成していなければ
            self._create_main_frm() #   メインフレームを生成
        self._start_update_status_label(self.main_frm)
    
    #   データ一覧フレームを表示
    def _show_data_list_frm(self):
        if self.data_list_frm:
            if self.after_cancel_id:
                self.root_frm.after_cancel(self.after_cancel_id)
            self.data_list_frm.pack()
        else:
            self.main_frm.pack_forget()
            self._create_data_list_frm()
        self._start_update_status_label(self.data_list_frm)
    
    #   パスワードフレームを表示
    def _show_pass_frm(self):
        self.main_frm.pack_forget()
        self._create_pass_frm()

    #   メンテナンスフレームを表示
    def _show_meintenance_frm(self):
        self._destroy_frm()
        self._create_maintenance_frm()
        self._start_update_status_label(self.maintenance_frm)
    
    #   良否判定フレームを表示
    def _show_judgemnt_result_frm(self):
        self.data_list_frm.pack_forget()
        self._create_judgment_result_frm()
        self._start_update_status_label(self.judgment_result_frm)
        self._create_result_today()
    
    #   寸法測定フレームを表示
    def _show_size_graph_frm(self):
        self.data_list_frm.pack_forget()
        self._create_size_graph_frm()
        self._start_update_status_label(self.size_graph_frm)
        self._show_graph()
    
    #   外観検査フレームを生成
    def _show_visul_inspection_frm(self):
        self.data_list_frm.pack_forget()
        self._create_visual_inspection_frm()
        self._start_update_status_label(self.visual_inspection_frm)
        self._update_visual_img()
    
    #   メインフレームに戻る
    def _return_main_frm(self):
        self._destroy_frm()
        self._show_frm(self.switching_main)

    #   データ一覧フレームに戻る
    def _return_data_list_frm(self):
        self._destroy_frm()
        self._show_frm(self.switching_data)
    
        # シリアル通信のデータ受信

    def recive(self):
        data1 = serial_conn1.get_receive_word()
        if data1:
            # 受信データを変数に格納→表示
            self.recv_plc_msg = struct.unpack('>B',data1)[0]
            print(f"PLCから受信:{self.recv_plc_msg}")
            data1 = ""
            self.case_chack()
            self.send()
        self.after_rcv_id = self.root_frm.after(1000,self.recive)  # 0.5秒ごとに更新        
    
    def send(self, send = None):
        if self.recv_plc_msg == b"s":    # インジケータ実行コマンド
            serial_conn2.set_send_word(b"s")    # 送信
            self.recive2 = serial_conn2.get_receive_word()
            print(f"インジケータから受信:{self.recive2}")
            self.recv_plc_msg = None
        elif self.recv_plc_msg:
            self.send_word = com.change_command(self.recv_plc_msg)
            if self.send_word:
                serial_conn1.set_send_word(self.send_word)
                self.send_word = None
            self.recv_plc_msg = None   
        elif send and self.error_flag != True:
            serial_conn1.set_send_word(send)
    
    def case_chack(self):
        if 0 <= self.recv_plc_msg and 100 >= self.recv_plc_msg:
            self.error()
        elif 100 < self.recv_plc_msg and 150 >= self.recv_plc_msg:
            # 動作開始命令用処理
            pass
        elif 150 < self.recv_plc_msg and 200 >= self.recv_plc_msg:
            # 動作終了伝達用処理
            pass
    
    def error(self):
        # ラベルの更新
        self.vitals_msg = msg.change_command(self.recv_plc_msg)
        # errorフラグON
        self.error_flag = True

    #   スタート関数
    def start(self):
        self._show_frm(self.switching_main)
        self.root_frm.protocol("WM_DELETE_WINDOW",self._click_close)
        self.root_frm.mainloop()


if __name__ == "__main__":
    # 各クラス作成
    meas = Meas()       #   デジタルインジケータ
    com = Com()         #   PlcComand
    msg = Commands()    #   エラーコマンド

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
