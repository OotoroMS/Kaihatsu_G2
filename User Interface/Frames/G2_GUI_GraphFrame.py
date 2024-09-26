import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# 寸法測定ログフレーム
class GraphFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        
        self.fig, self.ax = plt.subplots(figsize=(10, 7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.2, rely=0.2, anchor='nw')

        self.graph_update_id = None
    
        plt.rcParams['font.family'] = 'HGMaruGothicMPRO'
        plt.rcParams['font.size'] = 14
        plt.rcParams['axes.titlesize'] = 24
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['legend.fontsize'] = 12   
        
        self.create_widgets()
        self.setup_widgets()
        self.start_update_graph()
    
    # ウィジェットの作成
    def create_widgets(self):
        self.buttonR1 = tk.Button(self, text="戻る", font=("", 40), command=self.show_mode_frame)       
        
    # ウィジェットの配置
    def setup_widgets(self):
        self.buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)        
    
    # グラフを更新するためのデータを取得して描画
    def update_graph(self):
        size_list = []
        result = self.app.db.table_data_get('testdb_02', "select * from DB_sizelog order by id desc limit 50")
        for i in result:
            size_list.append(i[2])
        
        size_show = list(reversed(size_list))
        x = list(range(1, len(size_show) + 1))
        y = size_show
        yh = [0.1] * len(size_show)
        yl = [-0.1] * len(size_show)

        self.ax.clear()
        self.ax.plot(x, y, label='測定値')
        self.ax.plot(x, yh, label='上限')
        self.ax.plot(x, yl, label='下限')

        self.setup_graph()                    

    # グラフの軸ラベル、タイトル、凡例を設定
    def setup_graph(self):        
        self.ax.set_xlabel('直近50個')
        self.ax.set_ylabel('差異')
        self.ax.set_title('寸法測定ログ')

        self.ax.legend(loc='upper right')

        self.fig.tight_layout()

    # グラフを描画する
    def show_graph(self):
        self.update_graph()
        self.canvas.draw()
    
    # グラフの更新を定期的に実行
    def start_update_graph(self): 
        if self.graph_update_id is not None:
            self.after_cancel(self.graph_update_id)
            self.graph_update_id = None
        self.show_graph()    
        if self.winfo_ismapped():        
           self.graph_update_id = self.after(5000, self.start_update_graph)
    
    # ModeFrameを表示
    def show_mode_frame(self):
        self.app.show_frame(self.app.mode_frm)
