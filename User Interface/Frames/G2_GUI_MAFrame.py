import tkinter as tk

class MAFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.vital_msg = tk.StringVar()  # 必要に応じて初期化
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):        
        #   部品生成
        self.text01 = tk.Label(self,text="メンテナンス",font=("",55))
        self.buttonM1 = tk.Button(self,text="投入･洗浄部",font=("",40))
        self.buttonM2 = tk.Button(self,text="寸法検査部",font=("",40))
        self.buttonM3 = tk.Button(self,text="蓄積収納部",font=("",40))
        self.buttonM4 = tk.Button(self,text="外観検査部",font=("",40), command=self.show_ta01_frame)
        self.buttonM5 = tk.Button(self,text="手動トレーニング",font=("",40),command=self.show_man_tra_frame)
        self.buttonM6 = tk.Button(self,text="自動トレーニング",font=("",40),command=self.show_auto_tra_frame)
        self.buttonR1 = tk.Button(self, text="戻る", font=("", 40), command=self.show_main_frame)
        self.vital = self.app.vital_label  # Appからvital_labelを取得        

    def setup_widgets(self):
        #   部品配置
        self.text01.place(relx=0.3, rely=0.05, relwidth=0.2, relheight=0.1)
        self.buttonM1.place(relx=0.15, rely=0.25, relwidth=0.3, relheight=0.15)
        self.buttonM2.place(relx=0.15, rely=0.45, relwidth=0.3, relheight=0.15)
        self.buttonM3.place(relx=0.15, rely=0.65, relwidth=0.3, relheight=0.15)
        self.buttonM4.place(relx=0.55, rely=0.25, relwidth=0.3, relheight=0.15)
        self.buttonM5.place(relx=0.55, rely=0.45, relwidth=0.3, relheight=0.15)
        self.buttonM6.place(relx=0.55, rely=0.65, relwidth=0.3, relheight=0.15)
        self.buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    def show_main_frame(self):
        # メインフレームに戻る処理
        self.app.show_frame(self.app.main_frm)

    def show_auto_tra_frame(self):
        self.app.show_frame(self.app.auto_tra_frm)

    def show_man_tra_frame(self):
        self.app.show_frame(self.app.man_tra_frm)
    
    def show_ta01_frame(self):
        self.app.show_frame(self.app.ta01_frm)