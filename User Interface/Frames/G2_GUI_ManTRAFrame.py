import tkinter as tk

# 手動トレーニング用画面
class ManTRAFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.training_good_text = tk.StringVar()
        self.training_bad_text = tk.StringVar()
        self.training_good_text.set("良品カウント:0")
        self.training_bad_text.set("不良品カウント:0")
        self.training_good_cnt = 0
        self.training_bad_cnt = 0
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        # ウィジェットの設定はここ
        self.text01 = tk.Label(self, text="トレーニング", font=("", 55))
        self.text02 = tk.Label(self, textvariable=self.training_good_text, font=("", 30))
        self.text03 = tk.Label(self, textvariable=self.training_bad_text, font=("", 30))
        self.text04 = tk.Label(self, font=("", 30))
        self.buttonM1 = tk.Button(self, text="GOOD", font=("", 30), command=self.training_good_cnt_plus)
        self.buttonM2 = tk.Button(self, text="BAD", font=("", 30), command=self.training_bad_cnt_plus)
        self.buttonM3 = tk.Button(self, text="RUN", font=("", 30))
        self.buttonM4 = tk.Button(self, text="STOP", font=("", 30))
        self.buttonR2 = tk.Button(self, text="戻る", font=("", 40), command= self.show_ma_frame)        
        self.vital = self.app.vital_label  # Appからvital_labelを取得        

    def setup_widgets(self):
        # 部品を配置
        self.text01.place(relx=0.2, rely=0.05, relwidth=0.2, relheight=0.1)
        self.text02.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.1)
        self.text03.place(relx=0.6, rely=0.3, relwidth=0.2, relheight=0.1)
        self.text04.place(relx=0.3, rely=0.3)
        self.buttonM1.place(relx=0.15, rely=0.8, relwidth=0.1, relheight=0.1)
        self.buttonM2.place(relx=0.36, rely=0.8, relwidth=0.1, relheight=0.1)
        self.buttonM3.place(relx=0.6, rely=0.45, relwidth=0.2, relheight=0.1)
        self.buttonM4.place(relx=0.6, rely=0.57, relwidth=0.2, relheight=0.1)
        self.buttonR2.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)        

    def show_ma_frame(self):
        # メインフレームに戻る処理
        self.app.show_frame(self.app.ma_frm) 

    def training_good_cnt_plus(self):
        # 良品と判定したことを伝える

        self.training_good_cnt += 1
        # 上限値をいくつにするか未定
        if self.training_good_cnt >= 255:
            self.training_good_cnt = 0
            print("オーバーフロー")
        self.training_good_text.set(("良品カウント:",self.training_good_cnt))

    def training_bad_cnt_plus(self):
        # 不良品と判定したことを伝える

        self.training_bad_cnt += 1
        # 上限値をいくつにするか未定
        if self.training_bad_cnt >= 255:
            self.training_bad_cnt = 0
            print("オーバーフロー")
        self.training_bad_text.set(("不良品カウント:",self.training_bad_cnt))