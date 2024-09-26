class Commands:
    def __init__(self):
        # コマンド一覧と対応する数値(Serial用)
        self.commands = {
            1   :   4,
            2   :   5,
            3   :   6,
            'メンテナンス'  : 7
        }
        self.data = None    # コマンドに対応する数値を入れる
    
    def change_command(self, command):
        # 引数の値が辞書にあるか？
        if command in self.commands:
            # 引数の値に対応する数値を返す
            print(f"command:{command}, data:{self.data}")
            self.data = self.commands[command]
            return self.data             
        else:
            print("設定されていないコマンドです。")
            return None