import tkinter as tk
from tkinter import ttk

class TreeFrame(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app        
        self.count_7log = "select * from db_countlog order by id DESC limit 7"
        self.count_1log = "select * from db_now"
        self.error = "select * from db_timelog order by id DESC limit 50"
        self.data = None        
        self.error_data = None
        self.query = self.count_1log
        self.height = 250
        self.tree_update_id = None
        self.error_update_id = None        
        
        self.create_tree()
        self.create_widgets()
        self.setup_widgets()
        self.start_update_tree(self.count_1log, 250)

    def create_widgets(self):
        # ウィジェットを作成
        self.label = tk.Label(self, text="カウントログ", font=("", 70))
        self.tree = None  # TreeViewの初期化
        self.error_tree = None
        self.button_cr_today = tk.Button(self, text="本日の記録", font=("", 30), command=lambda: self.start_update_tree(self.count_1log, 250))
        self.button_cr_7days = tk.Button(self, text="七日間の記録", font=("", 27), command=lambda: self.start_update_tree(self.count_7log, 725))
        self.button_cr_badtime = tk.Button(self, text="不良発生の記録", font=("",25), command=self.start_update_error_tree)
        self.button_back = tk.Button(self, text="戻る", font=("", 40), command=self.show_mode_frame)        
        self.vital = self.app.vital_label  # Appからvital_labelを取得        

    def setup_widgets(self):
        # ウィジェットを配置
        self.label.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.1)
        self.button_cr_today.place(relx=0.02, rely=0.2, relwidth=0.12, relheight=0.12)
        self.button_cr_7days.place(relx=0.02, rely=0.34, relwidth=0.12, relheight=0.12)
        self.button_back.place(relx=0.85, rely=0.85, relwidth=0.1, relheight=0.1) 
        self.button_cr_badtime.place(relx=0.02,rely=0.48, relwidth=0.12, relheight=0.12)              

    def create_tree(self):
        self.columns = ('days', 'NO', 'good_size', 'bad_size', 'good_vision', 'bad_vision')
        self.headers = ['日付', '総個数', '寸法良', '寸法不良', '外観良', '外観不良']  
        self.error_columns = ('type', 'time')     
        self.error_headers = ['種類', '不良発生時間'] 
        self.style = ttk.Style()
        self.style.configure('Treeview.Heading', rowheight=100, font=("", 50))
        self.style.configure('Treeview', rowheight=160, font=("", 75))
        self.error_style = ttk.Style() 
        self.error_style.configure('Treeview.Heading',rowheight=40,font=("",40))
        self.error_style.configure('Treeview',rowheight=85,font=("",55))

    def update_tree(self):
        self.tree_destroy()

        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')

        for col, header in zip(self.columns, self.headers):
            self.tree.column(col, width=150, anchor='center')
            self.tree.heading(col, text=header, anchor='center')

        for item in self.data:
            self.tree.insert(parent='', index='end', values=item)
        self.tree.place(height=self.height, relx=0.57, rely=0.18, anchor=tk.N, relwidth=0.84)

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=0.99, rely=0.18, relheight=0.67, anchor=tk.N)

    def update_error_tree(self):
        self.tree_destroy()

        self.error_tree = ttk.Treeview(self, column=self.error_columns,show='headings')

        for col, header in zip(self.error_columns, self.error_headers):
            self.error_tree.column(col, width=124, anchor='center')
            self.error_tree.heading(col, text=header, anchor='center')

        for item in self.error_data:
            self.error_tree.insert(parent='', index='end', values=item)
        self.error_tree.place(height=self.height, relx=0.57, rely=0.18, anchor=tk.N, relwidth=0.84)

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.error_tree.yview)
        self.error_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=0.99, rely=0.18, relheight=0.67, anchor=tk.N)

    def start_update_tree(self, text="select * from db_now", height=250):
        self.update_cnacel()
        self.query = text
        self.height = height
        result = self.app.db.table_data_get('testdb_02', self.query)
        self.data = [(i[1][5:], i[2] + i[4], i[2], i[4], i[3], i[5]) for i in result if isinstance(i[1], str)]
        self.update_tree()
        if self.query == self.count_1log:
            if self.winfo_ismapped():
                self.tree_update_id = self.after(5000, self.start_update_tree)     

    def start_update_error_tree(self):
        self.update_cnacel()
        self.query = self.error
        self.height = 690 
        result = self.app.db.table_data_get('testdb_02', self.query)
        self.error_data = [(i[2], i[1][5:]) for i in result if isinstance(i[1], str)]
        self.update_error_tree()
        if self.winfo_ismapped():
            self.error_update_id = self.after(5000, self.start_update_error_tree)


    def update_cnacel(self):
        if self.tree_update_id is not None:
            self.after_cancel(self.tree_update_id)
            self.tree_update_id = None
        if self.error_update_id is not None:
            self.after_cancel(self.error_update_id)
            self.error_update_id = None

    def tree_destroy(self):
        if self.error_tree:
            self.error_tree.destroy()
            self.error_tree = None
        if self.tree:
            self.tree.destroy()
            self.tree = None

    def show_mode_frame(self):
        self.app.show_frame(self.app.mode_frm)
