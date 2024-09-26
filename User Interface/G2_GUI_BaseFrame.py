import tkinter as tk
from Frames.G2_GUI_MainFrame import MainFrame
from Frames.G2_GUI_ModeFrame import ModeFrame
from Frames.G2_GUI_GraphFrame import GraphFrame
from Frames.G2_GUI_TreeFrame import TreeFrame
from Frames.G2_GUI_VisionFrame import VisionFrame
from Frames.G2_GUI_PassFrame import PassFrame
from Frames.G2_GUI_MAFrame import MAFrame
from Frames.G2_GUI_ManTRAFrame import ManTRAFrame
from Frames.G2_GUI_AutoTRAFrame import AutoTRAFrame
from Frames.G2_GUI_TA01Frame import TA01Frame
import DbCommunication as DMC

class BaseFrame(tk.Tk):
    def __init__(self):
        # コンストラクタ: フルスクリーンの初期設定とフレーム作成を行う
        super().__init__()
        self.title('test')        
        self.attributes('-fullscreen', True)  
        self.db = DMC.DbCommunication()  
        self.update_vital_id = None  
        self.vital_label = None  
        self.current_frame = None  

        self.create_frame()  # 各フレームの作成
        self.create_widgets()  # ウィジェットの作成
        self.setup_widgets()  # ウィジェットの配置
        self.change_vital()  # 稼働状態の自動変更を開始

    # これを実行する
    def main(self, app):        
        app.mainloop()  # GUIの実行開始

    # ウィジェットの作成
    def create_widgets(self):
        self.vital_text = tk.StringVar(value="稼働中")  
        self.vital_color = tk.StringVar(value="red")  
        self.vital_label = tk.Label(self, textvariable=self.vital_text, font=("", 30), relief=tk.SOLID)  

    # ウィジェットの配置
    def setup_widgets(self):
        self.vital_label.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)  

    # 各フレームの作成
    def create_frame(self):
        self.main_frm = MainFrame(self, app=self)
        self.mode_frm = ModeFrame(self, app=self)
        self.graph_frm = GraphFrame(self, app=self)
        self.tree_frm = TreeFrame(self, app=self)
        self.vision_frm = VisionFrame(self, app=self)
        self.pass_frm = PassFrame(self, app=self)
        self.ma_frm = MAFrame(self, app=self)
        self.auto_tra_frm = AutoTRAFrame(self, app=self)
        self.man_tra_frm = ManTRAFrame(self, app=self)
        self.ta01_frm = TA01Frame(self, app=self)  

        self.current_frame = self.main_frm
        self.main_frm.pack(fill="both", expand=True)  

    # 引数に渡したフレームを表示
    def show_frame(self, frame):        
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        self.restart_after()
        self.vital_label.lift()

    # 各フレームの自動更新部分を再稼働
    def restart_after(self):
        if isinstance(self.current_frame, GraphFrame):
            self.after(1, self.current_frame.start_update_graph)
        if isinstance(self.current_frame, TreeFrame):
            self.after(1, self.current_frame.start_update_tree)
        if isinstance(self.current_frame, VisionFrame):
            self.after(1, self.current_frame.start_image_update)

    # GUIの終了
    def quit_application(self):        
        self.quit()

    # 稼働状態ラベルの自動変更(確認用)
    def change_vital(self):
        if self.update_vital_id is not None:
            self.after_cancel(self.update_vital_id)
            self.update_vital_id = None

        if self.vital_text.get() == "稼働中":
            self.vital_color.set("yellow")
            self.vital_text.set("停止中")
        elif self.vital_text.get() == "停止中":
            self.vital_color.set("yellow green")            
            self.vital_text.set("稼働中")
        self.vital_label.config(bg=self.vital_color.get())

        self.update_vital_id = self.after(5000, self.change_vital)

if __name__ == "__main__":
    app = BaseFrame()  # BaseFrameのインスタンスを作成
    app.main(app)   # main関数を実行 インスタンスを渡す
