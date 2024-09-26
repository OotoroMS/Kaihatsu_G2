import tkinter as tk
from tkinter import messagebox

# メインフレーム
class MainFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app        
        self.create_widgets()
        self.setup_widgets()                

    # ウィジェットの設定
    def create_widgets(self):
        self.text01 = tk.Label(self, text="検査・蓄積収納装置", font=("", 70))
        self.text02 = tk.Label(self, text="・データ閲覧", relief=tk.SOLID, anchor=tk.NW, font=("", 60))
        self.text03 = tk.Label(self, text="カウントログ", anchor=tk.W, font=("", 50))
        self.text04 = tk.Label(self, text="寸法検査ログ", anchor=tk.W, font=("", 50))
        self.text05 = tk.Label(self, text="外観検査ログ", anchor=tk.W, font=("", 50))
        self.text06 = tk.Label(self, text="・調査・動作確認", anchor=tk.W, font=("", 60))
        
        self.button1 = tk.Button(self, text="データ閲覧", font=("", 50), command=self.show_mode_frame)
        self.button2 = tk.Button(self, text="調査・動作確認", font=("", 50), command=self.click_vital)
        self.buttonf = tk.Button(self, text="終了", font=("", 40), command=self.quit_application)

        self.vital = self.app.vital_label  # Appからvital_labelを取得        

    # ウィジェットの配置
    def setup_widgets(self):
        self.text01.place(relx=0.22, rely=0.05, relwidth=0.4, relheight=0.1)
        self.text02.place(relx=0.5, rely=0.3, relwidth=0.32, relheight=0.45)
        self.text03.place(relx=0.55, rely=0.4, relwidth=0.2, relheight=0.06)
        self.text04.place(relx=0.55, rely=0.46, relwidth=0.25, relheight=0.06)
        self.text05.place(relx=0.55, rely=0.52, relwidth=0.25, relheight=0.06)
        self.text06.place(relx=0.501, rely=0.6, relwidth=0.31, relheight=0.1)                
        self.button1.place(relx=0.1, rely=0.3, relwidth=0.3, relheight=0.2)
        self.button2.place(relx=0.1, rely=0.6, relwidth=0.3, relheight=0.2)
        self.buttonf.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)        

    # 終了確認→終了
    def quit_application(self):
        if messagebox.askokcancel("確認", "終了しますか？"):
            self.app.quit_application()
    
    # データ閲覧画面を表示する処理
    def show_mode_frame(self):
        self.app.show_frame(self.app.mode_frm)
    
    # パスワード画面を表示する処理
    def show_pass_frame(self):
        self.app.show_frame(self.app.pass_frm)

    # Vitalメッセージの状態を確認し、必要に応じてパスワード画面に遷移
    def click_vital(self):
        if self.app.vital_text.get() != "停止中":            
            messagebox.showwarning("showwarning", "装置が安全な状態で再試行してください。")
        else:
            self.show_pass_frame()
