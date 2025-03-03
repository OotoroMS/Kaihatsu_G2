import json

def load_mae(filename):
    """JSON ファイルから 'mae' のリストを抽出する"""
    with open(filename, 'r') as f:
        data = json.load(f)['data']
    return [item['mae'] for item in data]

# ファイルから MAE 値を読み込み
flawless_mae = load_mae('flawless_test.json')
defective_mae = load_mae('defective_test.json')

n_flawless = len(flawless_mae)
n_defective = len(defective_mae)
total_samples = n_flawless + n_defective

# 全 MAE 値から候補閾値を作成
all_mae = flawless_mae + defective_mae
unique_values = sorted(set(all_mae))

candidates = set()

# 境界候補：最小値より少し下、最大値より少し上（浮動小数点誤差対策）
epsilon = 1e-6
candidates.add(unique_values[0] - epsilon)
candidates.add(unique_values[-1] + epsilon)

# 隣接する値の中間値を候補に追加
for i in range(len(unique_values) - 1):
    candidates.add((unique_values[i] + unique_values[i+1]) / 2)

# 一意な値自体も候補に追加
for val in unique_values:
    candidates.add(val)

candidates = sorted(candidates)

# 最適な閾値を求めるための初期化
best_cond1 = {'threshold': None, 'flawless_rate': -1}
best_cond2 = {'threshold': None, 'avg_rate': -1}
best_cond3 = {'threshold': None, 'overall_rate': -1}

# 各候補閾値で評価
for threshold in candidates:
    # 良品は MAE < threshold を良品と判定
    correct_flawless = sum(1 for mae in flawless_mae if mae < threshold)
    flawless_rate = correct_flawless / n_flawless
    
    # 不良品は MAE >= threshold を不良品と判定
    correct_defective = sum(1 for mae in defective_mae if mae >= threshold)
    defective_rate = correct_defective / n_defective

    overall_rate = (correct_flawless + correct_defective) / total_samples
    avg_rate = (flawless_rate + defective_rate) / 2

    # 条件1: 不良品検出率100%（floating point の誤差を考え、1.0に非常に近い場合とする）
    if defective_rate >= 0.999999:
        # この中で良品正答率が最大になる閾値を選ぶ
        if flawless_rate > best_cond1['flawless_rate']:
            best_cond1['threshold'] = threshold
            best_cond1['flawless_rate'] = flawless_rate

    # 条件2: 良品・不良品の正答率の平均が最大
    if avg_rate > best_cond2['avg_rate']:
        best_cond2['threshold'] = threshold
        best_cond2['avg_rate'] = avg_rate

    # 条件3: 全体の正答率が最大
    if overall_rate > best_cond3['overall_rate']:
        best_cond3['threshold'] = threshold
        best_cond3['overall_rate'] = overall_rate

# 結果の表示
print("【条件1】不良品検出率100%の中で、良品正答率が最大となる閾値:")
print("閾値:", best_cond1['threshold'])
print("良品正答率:", best_cond1['flawless_rate'])
print("不良品検出率: 100%")

print("\n【条件2】良品、不良品正答率の平均が最大となる閾値:")
print("閾値:", best_cond2['threshold'])
print("平均正答率:", best_cond2['avg_rate'])

print("\n【条件3】全体の正答率が最大となる閾値:")
print("閾値:", best_cond3['threshold'])
print("全体正答率:", best_cond3['overall_rate'])
