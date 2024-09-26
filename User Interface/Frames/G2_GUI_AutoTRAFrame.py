import tkinter as tk

# 自動トレーニングフレーム
class AutoTRAFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app  
        self.training_aout_text = tk.StringVar()  
        self.training_aout_text.set("動作回数:0")  
        self.training_aout_cnt = 0  
        self.create_widgets()  
        self.setup_widgets()  

    # ウィジェットの作成
    def create_widgets(self):
        self.text01 = tk.Label(self, text="トレーニング", font=("", 55))  
        self.text02 = tk.Label(self, textvariable=self.training_aout_text, font=("", 45))  
        self.text03 = tk.Label(self, font=("", 30))  
        self.buttonM1 = tk.Button(self, text="RUN", font=("", 30))  
        self.buttonM2 = tk.Button(self, text="STOP", font=("", 30))  
        self.buttonR2 = tk.Button(self, text="戻る", font=("", 40), command=self.show_ma_frame)  

    # ウィジェットの配置
    def setup_widgets(self):        
        self.text01.place(relx=0.2, rely=0.05, relwidth=0.2, relheight=0.1)  
        self.text02.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.1)  
        self.text03.place(relx=0.6, rely=0.3, relwidth=0.2, relheight=0.1)  
        self.buttonM1.place(relx=0.15, rely=0.8, relwidth=0.1, relheight=0.1)  
        self.buttonM2.place(relx=0.36, rely=0.8, relwidth=0.1, relheight=0.1)  
        self.buttonR2.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)  

    # MAFrameを表示
    def show_ma_frame(self):        
        self.app.show_frame(self.app.ma_frm)  
