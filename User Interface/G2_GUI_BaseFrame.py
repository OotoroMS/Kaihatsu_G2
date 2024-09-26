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
        super().__init__()
        self.title('test')
        # フルスクリーンに設定
        self.attributes('-fullscreen', True)
        self.db = DMC.DbCommunication()                            
        self.update_vital_id = None  
        self.vital_label = None
        self.current_frame = None           

        self.create_frame()
        self.create_widgets()
        self.setup_widgets()
        self.change_vital()       

    # これを呼んで実行
    def main(self):
        app = BaseFrame()
        app.mainloop()       

    def create_widgets(self):
        self.vital_text = tk.StringVar(value="稼働中")
        self.vital_color = tk.StringVar(value="red")
        self.vital_label = tk.Label(self, textvariable=self.vital_text, font=("", 30), relief=tk.SOLID)

    def setup_widgets(self):
        self.vital_label.place(relx=0.81, rely=0.06, relwidth=0.15, relheight=0.1)
        self.vital_label.lift()

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

        # 初期状態でMainFrameを表示
        self.current_frame = self.main_frm
        self.main_frm.pack(fill="both", expand=True)          

    def show_frame(self, frame):
        # 現在のフレームを非表示
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        # 指定されたフレームを表示
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        self.vital_label.lift()

        if isinstance(frame, GraphFrame):
            self.after(1, frame.start_update_graph)
        if isinstance(frame, TreeFrame):
            self.after(1, frame.start_update_tree)
        if isinstance(frame, VisionFrame):
            self.after(1, frame.start_image_update)

    def quit_application(self):        
        self.quit()

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
        self.vital_label.config(bg =self.vital_color.get())

        self.update_vital_id = self.after(5000, self.change_vital)

if __name__ == "__main__":
    app = BaseFrame()
    app.mainloop()
