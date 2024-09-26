import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class GraphFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        
        self.fig, self.ax = plt.subplots(figsize=(10, 7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(relx=0.2, rely=0.2, anchor='nw')

        self.graph_update_id = None
    
        # フォントの設定
        plt.rcParams['font.family'] = 'HGMaruGothicMPRO'
        plt.rcParams['font.size'] = 14
        plt.rcParams['axes.titlesize'] = 24
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['legend.fontsize'] = 12   
        
        self.create_widgets()
        self.setup_widgets()
        self.start_update_graph()
    
    def create_widgets(self):
        self.buttonR1 = tk.Button(self, text="戻る", font=("", 40), command=self.show_mode_frame)
        self.vital = self.app.vital_label  # Appからvital_labelを取得        
        
    def setup_widgets(self):
        self.buttonR1.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1)        
    
    def update_graph(self):
        size_list = []
        # self.app.dbを使ってデータベースからデータを取得
        result = self.app.db.table_data_get('testdb_02', "select * from DB_sizelog order by id desc limit 50")
        for i in result:
            size_list.append(i[2])
        
        size_show = list(reversed(size_list))
        x = list(range(1, len(size_show) + 1))
        y = size_show
        yh = [0.1] * len(size_show)
        yl = [-0.1] * len(size_show)

        # グラフの設定を最適化
        self.ax.clear()
        self.ax.plot(x, y, label='測定値')
        self.ax.plot(x, yh, label='上限')
        self.ax.plot(x, yl, label='下限')

        self.setup_graph()                    
    
    def setup_graph(self):        
        self.ax.set_xlabel('直近50個')
        self.ax.set_ylabel('差異')
        self.ax.set_title('寸法測定ログ')

        self.ax.legend(loc='upper right')

        # レイアウトを調整して、軸ラベルやタイトルが切れないようにする
        self.fig.tight_layout()

    def show_graph(self):
        self.update_graph()
        self.canvas.draw()
    
    def start_update_graph(self): 
        # 初回または有効なIDがある場合はキャンセル
        if self.graph_update_id is not None:
            self.after_cancel(self.graph_update_id)
            self.graph_update_id = None
        self.show_graph()    
        # 5秒ごとに更新
        if self.winfo_ismapped():        
           self.graph_update_id = self.after(5000, self.start_update_graph)
    
    def show_mode_frame(self):
        self.app.show_frame(self.app.mode_frm)