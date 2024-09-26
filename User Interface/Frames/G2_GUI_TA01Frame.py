import tkinter as tk

class TA01Frame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.create_widgets()
        self.setup_widgets()

    # ウィジェットの作成
    def create_widgets(self):
        self.text01 = tk.Label(self,text="メンテナンス01",font=("",55))
        self.buttonM1 = tk.Button(self,text="動作01",font=("",40))
        self.buttonM2 = tk.Button(self,text="動作02",font=("",40))
        self.buttonM3 = tk.Button(self,text="動作03",font=("",40))
        self.buttonM4 = tk.Button(self,text="動作04",font=("",40))
        self.buttonM5 = tk.Button(self,text="動作05",font=("",40))
        self.buttonM6 = tk.Button(self,text="動作06",font=("",40))
        self.buttonR2 = tk.Button(self,text="戻る",font=("",40),command=self.show_ma_frame)       
    # ウィジェットの配置        
    def setup_widgets(self):
        self.text01.place(relx=0.3, rely=0.05, relwidth=0.3, relheight=0.1)
        self.buttonM1.place(relx=0.15, rely=0.25, relwidth=0.25, relheight=0.12)
        self.buttonM2.place(relx=0.15, rely=0.45, relwidth=0.25, relheight=0.12)
        self.buttonM3.place(relx=0.15, rely=0.65, relwidth=0.25, relheight=0.12)
        self.buttonM4.place(relx=0.55, rely=0.25, relwidth=0.25, relheight=0.12)
        self.buttonM5.place(relx=0.55, rely=0.45, relwidth=0.25, relheight=0.12)
        self.buttonM6.place(relx=0.55, rely=0.65, relwidth=0.25, relheight=0.12)
        self.buttonR2.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    # MAFrameを表示
    def show_ma_frame(self):
        self.app.show_frame(self.app.ma_frm)