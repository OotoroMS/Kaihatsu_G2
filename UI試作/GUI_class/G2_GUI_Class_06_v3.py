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

import threading
from SerialConnection import SerialConnection as Serial
from Measurement import Meas
from commands import Commands as Com

# 画面サイズの定義
WIDTH = 900
HEIGHT = 600

# シリアル通信用
PORT1 = "COM4"  # PC用
PORT2 = "COM6"  # Digital用
BAUD_RATE1 = 9600  # ボーレート 9600
BAUD_RATE2 = 2400  # ボーレート 2400
TIMEOUT = 1  # タイムアウト時間

class App(tki.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title('test')
        self.root.attributes('-fullscreen', True)
        root.grid_rowconfigure(0, weight=1)  # 行の重みを設定
        root.grid_columnconfigure(0, weight=1)  # 列の重みを設定

        # シリアル通信用
        self.recive1 = None
        self.send1 = None
        self.recive2 = None
        self.send2 = None
        self.send_word = None

        # 各フラグをセルフにしました
        self.flag_01 = 0
        self.flag_02 = 0
        self.flag_03 = 0

        # 初期化
        self.cancel_flag = None
        self.tree = None

        # figをセルフ化
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.fig.tight_layout()
        self.canvas = None

        # それぞれのフレームの初期化を行いました
        self.main_frm = tki.Frame(self.root)
        self.work_mode_frm = tki.Frame(self.root)
        self.size_log_frm = tki.Frame(self.root)
        self.vision_frm = tki.Frame(self.root)
        self.count_frm = tki.Frame(self.root)
        self.admin_mode_frm = tki.Frame(self.root)

        # 各フレームの作成をまとめたよ
        self.creat_main_frm()
        self.creat_work_mode_frm()
        self.creat_size_log_frm()
        self.creat_vision_frm()
        self.creat_count_frm()
        self.creat_admin_mode_frm()

        # フレームレイアウトを設定
        self.main_frm.grid(row=0, column=0, sticky='nsew')
        self.work_mode_frm.grid(row=0, column=0, sticky='nsew')        
        self.size_log_frm.grid(row=0, column=0, sticky='nsew')
        self.vision_frm.grid(row=0, column=0, sticky='nsew')
        self.count_frm.grid(row=0, column=0, sticky='nsew')        
        self.admin_mode_frm.grid(row=0, column=0, sticky='nsew')

        # メインフレームの表示をここでやってるよ
        self.show_main_frm()
    
    def creat_main_frm(self):
        # メインフレームのウィジェットの作成
        text1 = tki.Label(self.main_frm,text="検査・蓄積収納装置",font=("",20))   #Label-テキスト
        button1 = tki.Button(self.main_frm,text="データ閲覧",
                            #style="sample.TButton",
                            font=("",20),
                            command=self.show_work_mode_frm)      #Button-ボタン
        button2 = tki.Button(self.main_frm,text="メンテナンス",
                            font=("",20),
                            command=self.show_admin_mode_frm)
        textbox1 = tki.Label(self.main_frm,text=
                            "・データ閲覧\n カウントログ \n寸法検査ログ\n外観検査ログ\n\n ・メンテナンス"
                            ,font=("",20))
        buttonf = tki.Button(self.main_frm,text="終了",command=self.click_close)

        #配置 relx-x座標 rely-y座標 rewidth-幅 reheight-高さ  0.0~1.0
        text1.place(relx=0.4, rely=0.05, relwidth=0.5, relheight=0.1)
        button1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.2)
        button2.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
        textbox1.place(relx=0.6, rely=0.2)#, relwidth=0.3, relheight=0.5
        buttonf.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def creat_work_mode_frm(self):
        # データ閲覧フレームのウィジェットの作成
        text1 = tki.Label(self.work_mode_frm,text="データ閲覧",font=("",20))
        buttonc = tki.Button(self.work_mode_frm,text="カウントログ",
                            command=self.show_count_frm)             #c-count
        buttons = tki.Button(self.work_mode_frm,text="寸法検査ログ",
                            command=self.show_size_log_frm)             #s-size
        buttone = tki.Button(self.work_mode_frm,text="外観検査ログ",
                            command=self.show_vision_frm)       #e-exterior
        buttonR = tki.Button(self.work_mode_frm,text="戻る",command=self.show_main_frm)

        # 配置
        text1.place(relx=0.4, rely=0.05, relwidth=0.5, relheight=0.1)
        buttonc.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)
        buttons.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)
        buttone.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.1)
        buttonR.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def creat_size_log_frm(self):
        # 寸法測定ログフレームのウィジェットの作成
        buttonR1 = tki.Button(self.size_log_frm,text="戻る",command=self.show_work_mode_frm)

        # 配置
        buttonR1.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)

    def creat_vision_frm(self):
        # 外観検査ログフレームのウィジェットの作成
        buttonR1 = tki.Button(self.vision_frm,text="戻る",command=self.show_work_mode_frm)

        # 配置
        buttonR1.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
    
    def creat_count_frm(self):
        # カウントログフレームのウィジェットの作成
        button_cr_today = tki.Button(self.count_frm,text="本日の記録",command=self.count_log)
        button_cr_7days = tki.Button(self.count_frm,text="火の七日間",command=self.count_log_7_days)
        buttonR1 = tki.Button(self.count_frm,text="戻る",command=self.show_work_mode_frm)

        # 配置
        # self.count_vitals.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        buttonR1.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
        button_cr_today.place(relx=0.1,rely=0.8, relwidth=0.1, relheight=0.1)
        button_cr_7days.place(relx=0.25,rely=0.8, relwidth=0.1, relheight=0.1)

    def creat_admin_mode_frm(self):
        # メンテナンスフレームのウィジェットの作成
        text1 = tki.Label(self.admin_mode_frm,text="メンテナンス",font=("",20))
        buttonR1 = tki.Button(self.admin_mode_frm,text="戻る",command=self.show_main_frm)
        button1 = tki.Button(self.admin_mode_frm,text="1",command=lambda:self.send(1))
        button2 = tki.Button(self.admin_mode_frm,text="2",command=lambda:self.send(2))
        button3 = tki.Button(self.admin_mode_frm,text="3",command=lambda:self.send(3))

        # 配置
        text1.place(relx=0, rely=0.05, relwidth=0.2, relheight=0.1)
        buttonR1.place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.1)
        button1.place(relx=0.1,rely=0.8, relwidth=0.1, relheight=0.1)
        button2.place(relx=0.25,rely=0.8, relwidth=0.1, relheight=0.1)
        button3.place(relx=0.4,rely=0.8, relwidth=0.1, relheight=0.1)        

    # フレーム切替
    def show_frm(self, frm):
        # 引数のフレームを表示
        frm.tkraise()

    # メインフレーム表示
    def show_main_frm(self):
        self.show_frm(self.main_frm)
    
    # モード選択フレーム表示
    def show_work_mode_frm(self):
        self.show_frm(self.work_mode_frm)
        self.flag_01 = 0
        self.flag_02 = 0
        self.flag_03 = 0

    # 寸法測定フレーム表示
    def show_size_log_frm(self):
        self.show_frm(self.size_log_frm)  
        self.show_size_log_graph()
        self.flag_02=1       

    # 外観検査フレーム表示
    def show_vision_frm(self):
        self.show_frm(self.vision_frm)
        self.flag_01=1
        self.vision_up()

    # 管理者フレーム表示
    def show_admin_mode_frm(self):
        self.show_frm(self.admin_mode_frm)

    # カウントフレーム表示
    def show_count_frm(self):
        self.show_frm(self.count_frm)
        if self.tree:
            self.tree.destroy()
        if self.cancel_flag:
            self.root.after_cancel(self.cancel_flag)
        self.count_log()

    # 終了確認表示
    def click_close(self):
        if messagebox.askokcancel("確認","終了しますか？"):
            self.cleanup_canvas()  # キャンバスとフィギュアのクリーンアップ
            self.root.destroy()

    def cleanup_canvas(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()  # キャンバスを削除
            self.canvas = None  # self.canvas を None に設定
        if self.fig:
            plt.close(self.fig)  # Figure を閉じる
            self.fig = None  # self.fig を None に設定

    def graph(self):
        size_list = []
        result = db.table_data_get('testdb_02', "select * from DB_sizelog order by id desc limit 10")
        for i in result:
            size_list.append(i[2])
        
        size_show = list(reversed(size_list))
        x = list(range(1, len(size_show) + 1))
        y = size_show
        yh = [0.1] * len(size_show)
        yl = [-0.1] * len(size_show)
        
        # フォントの設定
        plt.rcParams['font.family'] = 'HGMaruGothicMPRO'
        plt.rcParams['font.size'] = 14
        plt.rcParams['axes.titlesize'] = 24
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['legend.fontsize'] = 12

        # グラフの設定を最適化
        self.ax.clear()
        self.ax.plot(x, y, label='測定値')
        self.ax.plot(x, yh, label='上限')
        self.ax.plot(x, yl, label='下限')

        self.ax.set_xlabel('直近10個')
        self.ax.set_ylabel('差異')
        self.ax.set_title('寸法測定ログ')

        self.ax.legend(loc='upper right')

        # レイアウトを調整して、軸ラベルやタイトルが切れないようにする
        self.fig.tight_layout()    


    def show_size_log_graph(self):
        self.graph()
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.size_log_frm)
        self.canvas.get_tk_widget().place(relx=0.2, rely=0.2, anchor='nw')
        self.canvas.draw()
        if self.flag_02 == 1:
            self.root.after(5000, self.show_size_log_graph)
    
    def update_tree(self, columns, headers, data, frame, height):
        if self.cancel_flag:
            self.root.after_cancel(self.cancel_flag)
        if self.tree:
            self.tree.destroy()

        self.tree = ttk.Treeview(frame, columns=columns, show='headings')

        style = ttk.Style()
        style.configure('Treeview.Heading', font=("", 20))
        style.configure('Treeview', rowheight=50, font=("", 30))

        for col, header in zip(columns, headers):
            self.tree.column(col, width=140, anchor='center')
            self.tree.heading(col, text=header, anchor='center')

        for item in data:
            self.tree.insert(parent='', index='end', values=item)        
        self.tree.place(height=height, relx=0.5, rely=0.02, anchor=tki.N, relwidth=0.9)

    def count_log_7_days(self):
        columns = ('days', 'NO', 'good_size', 'bad_size', 'good_vision', 'bad_vision')
        headers = ['日付', '総個数', '寸法良', '寸法不良', '外観良', '外観不良']
        query = "select * from db_countlog order by id DESC limit 7"
        result = db.table_data_get('testdb_02', query)

        data = [(i[1][5:], i[2] + i[4], i[2], i[4], i[3], i[5]) for i in result if isinstance(i[1], str)]
        
        self.update_tree(columns, headers, data, self.count_frm, 500)

        if self.flag_03 == 1:
            self.cancel_flag = self.root.after(5000, self.count_log_7_days)

    def count_log(self):
        columns = ('days','NO', 'good_size', 'bad_size', 'good_vision', 'bad_vision')
        headers = ['日付', '総個数', '寸法良', '寸法不良', '外観良', '外観不良']
        query = "select * from db_now"
        result = db.table_data_get('testdb_02', query)

        data = [(i[1][5:], i[2] + i[4], i[2], i[4], i[3], i[5]) for i in result if isinstance(i[1], str)]

        self.update_tree(columns, headers, data, self.count_frm, 150)

        if self.flag_03 == 1:
            self.cancel_flag = self.root.after(5000, self.count_log)  

    #   外観検査画像表示処理
    def vision_up(self):
        dir_path = Path("D:/kaihatu/test/UI/img_file")
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
        img1=Image.open("D:/kaihatu/test/UI/img_file/"f"/{list_date_new}.jpg")
        w_size = int(img1.width/4)
        h_size = int(img1.height/4)
        self.ttk_img = None
        self.ttk_img=ImageTk.PhotoImage(image=img1.resize((w_size,h_size))) # Pillowで読み込んだ画像をtkinterで表示できるよう設定
        cvs=tki.Canvas(self.vision_frm,width=w_size-2,height=h_size-2,bg="red")# tkinterは標準でJPEGを表示できないため
        cvs.create_image(0,0,image=self.ttk_img,anchor=tki.NW)
        cvs.place(relx=0.3,rely=0.25,anchor=tki.NW)

        #rootform.after(1000,vision_up)#5秒ごとに処理
        print(self.flag_01)
        if(self.flag_01 == 1):
            self.cansel_id = self.root.after(5000,self.vision_up)    #5秒ごとに処理 

    # シリアル通信のデータ受信
    def recive(self):
        data1 = serial_conn1.get_receive_word() 
        if data1:
            # 受信データを変数に格納→表示
            self.recive1 = data1
            print(f"PLCから受信:{self.recive1}")
            data1 = ""
            self.after(500,self.send(None))
        self.after(500,self.recive)  # 0.5秒ごとに更新        
    
    def send(self, send):
        if self.recive1 == b"s":    # インジケータ実行コマンド
            serial_conn2.set_send_word(b"s")    # 送信
            self.recive2 = serial_conn2.get_receive_word()
            print(f"インジケータから受信:{self.recive2}")
            self.recive1 = None
        elif self.recive1:
            self.send_word = Com.change_command(self.recive1)
            if self.send_word:
                serial_conn1.set_send_word(self.send_word)
                self.send_word = None
            self.recive1 = None   
        elif send:
            serial_conn1.set_send_word(send)            


# デジタルインジケータのクラス作成
meas = Meas()

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

root = tki.Tk()
app = App(root)
app.recive()
# app.send(None)
root.mainloop()

# シリアル通信終了処理
serial_conn1.shutdown_flag = True
serial_conn2.shutdown_flag = True

if serial_conn1.is_open:
    serial_conn1.close()
if serial_conn2.is_open:
    serial_conn2.close()

print("プログラムを終了します.")