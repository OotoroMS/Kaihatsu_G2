import tkinter as tk
from tkinter import messagebox

class PassFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.input_pass = tk.StringVar()
        self.positions = [(0.355, 0.76), (0.295, 0.65), (0.405, 0.65), (0.515, 0.65), (0.295, 0.54), 
                     (0.405, 0.54), (0.515, 0.54), (0.295, 0.43), (0.405, 0.43), (0.515, 0.43)]
        self.create_widgets()
        self.setup_widgets()

    # ウィジェットの作成
    def create_widgets(self):
        self.label_title = tk.Label(self, text="パスワード入力", font=("", 50))
        self.label_pass = tk.Label(self, textvariable=self.input_pass, font=("", 45), name="pass", relief=tk.SOLID)                
        self.button_reset = tk.Button(self, text="Reset", font=("", 30), command=lambda: self.set_pass("r"))
        self.button_enter = tk.Button(self, text="Enter", font=("", 30), command=self.judge_pass)
        self.button_back = tk.Button(self, text="戻る", font=("", 40), command=self.show_main_frame)                    
        self.buttons = [tk.Button(self, text=f"{i}", font=("", 50), command=lambda j=i: self.set_pass(f"{j}")) for i in range(10)]        

    # ウィジェットの配置
    def setup_widgets(self):
        self.label_title.place(relx=0.25, rely=0.05, relwidth=0.4, relheight=0.1)
        self.label_pass.place(relx=0.35, rely=0.25, relwidth=0.25, relheight=0.1)                        
        self.buttons[0].place(relwidth=0.2, relheight=0.1)
        self.button_reset.place(relx=0.65, rely=0.43, relwidth=0.1, relheight=0.2)
        self.button_enter.place(relx=0.65, rely=0.65, relwidth=0.1, relheight=0.2)
        self.button_back.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)        
        for i, btn in enumerate(self.buttons):
            btn.place(relx=self.positions[i][0], rely=self.positions[i][1], relwidth=0.1, relheight=0.1)                

    # 数字ボタン+リセットボタン処理
    def set_pass(self, value):
        str_pass = self.input_pass.get()
        if value == "r":
            str_pass = ""
        elif value:
            str_pass += value        
        self.input_pass.set(str_pass)

    # パスワード判定
    def judge_pass(self):
        if self.input_pass.get() == "2024":
            self.show_ma_frame()
            self.input_pass.set("")
        else:
             messagebox.showwarning("warning", "パスワードが間違っています。")

    # MainFrameを表示
    def show_main_frame(self):        
        self.app.show_frame(self.app.main_frm)

    # ManTRAFrameを表示
    def show_ma_frame(self):
        self.app.show_frame(self.app.ma_frm)
