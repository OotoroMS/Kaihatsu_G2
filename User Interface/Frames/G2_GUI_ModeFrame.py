import tkinter as tk
from tkinter import messagebox

class ModeFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.create_widgets()
        self.setup_widgets()

    def create_widgets(self):
        # ウィジェットの設定はここ
        self.text01 = tk.Label(self,text="データ閲覧",font=("",70))
        #   ボタン
        self.buttonc = tk.Button(self,text="カウントログ",font=("",50), command=self.show_tree_frame)
        self.buttons = tk.Button(self,text="寸法検査ログ",font=("",50), command=self.show_graph_frame)
        self.buttone = tk.Button(self,text="外観検査ログ",font=("",50), command=self.show_vision_frame)
        self.buttonR = tk.Button(self,text="戻る",font=("",40), command=self.show_main_frame)
        self.vital = self.app.vital_label  # Appからvital_labelを取得        
        
    def setup_widgets(self):
        # 部品を配置
        self.text01.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)        
        self.buttonc.place(relx=0.1, rely=0.25, relwidth=0.3, relheight=0.1)
        self.buttons.place(relx=0.1, rely=0.45, relwidth=0.3, relheight=0.1)
        self.buttone.place(relx=0.1, rely=0.65, relwidth=0.3, relheight=0.1)
        self.buttonR.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)

    def show_main_frame(self):
        # App の show_frame メソッドを呼び出す
        self.app.show_frame(self.app.main_frm)

    def show_graph_frame(self):
        # App の show_frame メソッドを呼び出す
        self.app.show_frame(self.app.graph_frm)

    def show_tree_frame(self):
        self.app.show_frame(self.app.tree_frm)

    def show_vision_frame(self):
        self.app.show_frame(self.app.vision_frm)