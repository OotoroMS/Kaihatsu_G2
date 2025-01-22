
class Compare:
    def __init__():
        # ここでDataBaseのクラスをインスタンス化する？
        # いやBase/で制御した方がいいと思う
        pass
    
    # data: 測定値(差) default_data: 基準値(データベースから取得)
    @staticmethod
    def main(data: float, default_data: float) -> str:
        max = default_data + 0.1
        min = default_data - 0.1
        dif = default_data - data
        if dif > max or dif < min:
            return "NG"
        return "OK"