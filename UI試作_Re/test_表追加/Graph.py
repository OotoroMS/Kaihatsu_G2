import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import DbCommunication as DMC #DB関係
import multiprocessing
import time

DETABESE = "testdb_02"
QUERY = "select * from DB_sizelog order by id desc limit 20"

#   グラフを生成
def create_graph():
    graph_data = get_data()
    data_list = get_list(graph_data)
    x,y,yh,yl = create_data(data_list)
    create_fig(x,y,yh,yl)

#   データベースからデータを取得
def get_data():
    db = DMC.DbCommunication()
    result = db.table_data_get(DETABESE, QUERY)
    return result

#   寸法検査の結果を抽出したリストを生成
def get_list(result):
    #   寸法検査結果のみを抽出
    list_size = list()
    for i in result:
        list_size.append(i[2])
    return list(reversed(list_size))

#   グラフ描画に使用するデータを生成
def create_data(list_size:list):
    x = list(range(1,21))
    y = list_size
    yh = list()
    yl = list()
    for i in range(0,20,1):
        yh.append(0.1)
        yl.append(-0.1)
    return x,y,yh,yl

#   グラフを描画
def create_fig(x,y,yh,yl):
    plt.close()
    plt.figure(figsize=(10,8))
    plt.rcParams['font.family'] = 'HGMaruGothicMPRO'
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.titlesize'] = 24
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['legend.fontsize'] = 12
    plt.plot(x, y, label="測定値")
    plt.plot(x,yh, label="上限")
    plt.plot(x,yl, label="下限")
    plt.xlabel("直近20個")
    plt.ylabel("測定値")
    plt.title("寸法測定ログ")
    plt.legend(loc='upper left', bbox_to_anchor=(0, 1))

    plt.savefig("D:\\GitHub\\Kaihatsu_G2\\UI試作_Re\\test_表追加\\graph.png", format='png')
    plt.close()

class Graph:
    #   初期設定
    def __init__(self):
        self.stop_event = multiprocessing.Event()
        self.graph_thread = None
    
    #   マルチプロセス使用時に指定
    def start_graph_thread(self):
        self.create_and_load_graph()
    
    #   グラフを更新
    def create_and_load_graph(self):
        while not self.stop_event.is_set():
            create_graph()
            time.sleep(1)

        plt.close()
        print("end plocess")
    #   マルチプロセス終了関数
    def stop_graph_thread(self):
        # プロセスを終了するためにフラグを立てる
        self.stop_event.set()