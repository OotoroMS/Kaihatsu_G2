import os
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk

class VisionFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app     
        self.ttk_img = None   
        self.image_update_id = None

        self.create_widgets()
        self.setup_widgets()
        self.start_image_update()

    # ウィジェットの作成
    def create_widgets(self):
        self.buttonR1 = tk.Button(self, text="戻る", font=("", 40), command=self.show_mode_frame)        
        self.canvas = tk.Canvas(self, bg="red")  # 画像を表示するキャンバスを作成       
    
    # ウィジェットの配置
    def setup_widgets(self):        
        self.buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)
        self.canvas.place(relx=0.1, rely=0.1, relwidth=0.535, relheight=0.7)        

    # 画像を定期的に更新
    def start_image_update(self):
        if self.image_update_id is not None:
            self.after_cancel(self.image_update_id)
            self.image_update_id = None
        self.update_image()
        if self.winfo_ismapped():
            self.image_update_id = self.after(5000, self.start_image_update)        

    # 画像のデータをもってきて表示
    def update_image(self):
        dir_path = Path("C:/Users/is2306/Documents/GitHub/Kaihatsu_G2/User Interface/img_file")
        files = list(dir_path.glob("*.jpg"))
        
        if files:
            latest_file = sorted(files, key=lambda f: f.stem, reverse=True)[0]
            img = Image.open(latest_file)
            img_resized = img.resize((int(img.width / 2.5), int(img.height / 2.5)))
            self.ttk_img = ImageTk.PhotoImage(img_resized)
            self.canvas.create_image(0, 0, image=self.ttk_img, anchor=tk.NW)
        else:
            self.canvas.delete("all")
            self.canvas.create_text(500, 60, text="NO_image", fill="white", font=("", 70))

    # ModeFrameを表示
    def show_mode_frame(self):
        self.app.show_frame(self.app.mode_frm)
