#グラフ表示のための設定(オプションのUIでは使わない)
import matplotlib
import matplotlib.pyplot as plt
from DB.SQLCommunication import SQLCommunication as SQL

matplotlib.use('Agg')

SIZE = (13,7.5)
DB = "testdb_main.db"
QUERY = "select * from DB_sizelog order by id desc limit 20"
FONT = 'HGMaruGothicMPRO'
PATH = "GUI_main_test\\image\\graph.png"

#   データベースからデータを取得
def get_data():
    db = SQL()
    result = db.db_query_execution(DB, QUERY)
    return result

#   寸法測定値を取り出す
def get_meas_result(result):
    meas_result = list()
    for i in result:
        meas_result.append(i[2])
    return meas_result

#   良否判定の上限と下限の線を生成
def limit_line():
    yh = list()
    yl = list()
    for i in range(0,20,1):
        yh.append(0.1)
        yl.append(-0.1)
    return yh, yl

#   グラフの設定を変更
def config_graph():
    plt.rcParams['font.family'] = FONT
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.titlesize'] = 24
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['legend.fontsize'] = 12

#   グラフの線を描画
def draw_graph(x,y,yh,yl):
    plt.plot(x, y, label="測定値")
    plt.plot(x,yh, label="上限")
    plt.plot(x,yl, label="下限")

#   ラベルを描画
def draw_label():
    plt.xlabel("直近20個")
    plt.ylabel("測定値")
    plt.title("寸法測定ログ")
    plt.legend(loc='upper left', bbox_to_anchor=(0, 1))

#   保存してグラフを削除
def save_graph():
    plt.savefig(PATH, format='png')
    plt.close()

#   グラフを作成して保存
def create_graph(x,y,yh,yl):
    plt.figure(figsize=SIZE)
    config_graph()
    draw_graph(x,y,yh,yl)
    draw_label()
    save_graph()

def graph():
    db_result = get_data()
    x = list(range(1,21))
    y = get_meas_result(db_result)
    yh, yl = limit_line()
    create_graph(x,y,yh,yl)

if __name__ == "__main__":
    graph()