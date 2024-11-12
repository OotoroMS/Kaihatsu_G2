import serial
import time

class RotationControl:
    def __init__(self, port, baudrate=9600, timeout=1):
        """
        :param port: PLCが接続されているシリアルポート
        :param baudrate: 通信速度（ボーレート）
        :param timeout: シリアル通信のタイムアウト時間（秒）
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        
        # シリアル接続の初期化
        self.serial_connection = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def send_rotation_command(self, command):
        """
        PLCに回転コマンドを送信する
        :param command: PLCに送信する回転コマンド（文字列）
        """
        if self.serial_connection.isOpen():
            self.serial_connection.write(command.encode())
            print(f"Command sent: {command}")
        else:
            raise RuntimeError("Serial connection is not open.")

    def close_connection(self):
        """
        シリアル接続を閉じる
        """
        if self.serial_connection and self.serial_connection.isOpen():
            self.serial_connection.close()

if __name__ == "__main__":
    try:
        # 回転制御モジュールのインスタンス作成
        rotation_control = RotationControl(port='COM3', baudrate=9600)

        # モーターを回転させるコマンドを送信（例: 時計回りに回転）
        rotation_control.send_rotation_command('ROTATE_CW_512')
        
        # 少し待機してから反時計回りに回転させるコマンドを送信
        time.sleep(1)
        rotation_control.send_rotation_command('ROTATE_CCW_512')
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # シリアル接続を閉じる
        rotation_control.close_connection()