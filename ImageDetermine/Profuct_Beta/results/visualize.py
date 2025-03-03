import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# JSON ファイルから MAE 値を読み込む関数
def load_mae(filename):
    with open(filename, 'r') as f:
        data = json.load(f)['data']
    return [item['mae'] for item in data]

# 各ファイルから MAE 値を取得
flawless_mae = load_mae('flawless_test.json')
defective_mae = load_mae('defective_test.json')

# DataFrame を作成（'type' 列で区別）
df_flawless = pd.DataFrame({'mae': flawless_mae, 'type': 'flawless'})
df_defective = pd.DataFrame({'mae': defective_mae, 'type': 'defective'})
df_all = pd.concat([df_flawless, df_defective], ignore_index=True)

# それぞれの統計量（件数、平均、標準偏差、最小値、四分位数、最大値）を表示する表
stats = df_all.groupby('type')['mae'].describe()
print("=== MAE の統計量 ===")
print(stats)

# グラフの描画設定
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")

# ヒストグラム＋カーネル密度推定（KDE）を type 別に描画
sns.histplot(data=df_all, x='mae', hue='type', bins=30, kde=True, stat="density", common_norm=False)

plt.xlabel("MAE")
plt.ylabel("Density")
plt.title("Flawless と Defective の MAE 分布")
plt.legend(title='Type')
plt.tight_layout()
plt.show()
