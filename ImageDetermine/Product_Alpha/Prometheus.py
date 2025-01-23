# 外観検査ライブラリ

# ライブラリのインポート
import numpy as np
import cv2
import tensorflow as tf
import threading
import time
import json
import os
import serial
from datetime import datetime 

# 自作ライブラリのインポート
import ImgDtrmn_Lib as ImgDtrmn_Lib
import Cmr_Lib as Cmr_Lib
import serial_communicator as PLC_Lib
from pc_comands import PCManager
#import SQLCommunication as SQLComm
import serial_gate


# 定数
DB_NAME = ""  # データベース名(未設定のため、のちに作成)

# グローバル変数
COM_CMR = 0             # カメラのデバイス番号（デフォルトカメラを使用）

# 変数の初期化（後で設定ファイルから読み込む）
WORK_NAME = ""          # ワーク名
MDL_PATH = ""           # モデルのパス
ROTATE_DEGREE = 0       # 回転角度
ROTATE_COUNT = 0        # 回転回数
CROP_RANGES = []        # クロップ範囲

JUDGE = {               # 判定結果
    "OK": True,
    "NG": False,
}

PLC_SND_CMD = {         # PLC送信コマンド
    "EXIST": b'\x0b',
    "NOT EXIST": b'\x0c',
    "FLAWLESS": b'\x14',
    "DEFECTIVE": b'\x15',
    "ROTATE": b'\xdd',
}

PLC_RCV_CMD = {         # PLC受信コマンド
    "CHECK_EXIST": b'\xc8',
    "SET WORK": b'\xd2',
}

THRESHOLD = 0.003        # 判別閾値

captured_image = None   # 撮影した画像
infered_accuracy = 0    # 推論結果
infered_image = None    # 推論画像
init_image = None       # 初期状態の背景画像


class Prometheus:
    # コンストラクタ
    def __init__(self, stop_event: threading.Event):
        self.stop_event = stop_event
        pass        

    # 設定ファイルの読み込み
    def load_config():
        global MDL_PATH, ROTATE_DEGREE, ROTATE_COUNT, THRESHOLD, CROP_RANGES
        # determine_config.jsonを読み込む
        with open('determine_config.json', 'r') as f:
            config = json.load(f)
            
        WORK_NAME = config['work_name']
        ROTATE_DEGREE = config['rotate_degree']
        ROTATE_COUNT = config['rotate_count']
        work_config = config['work_config_file']
        
        # ワークの詳細設定ファイルを読み込む
        with open(work_config, 'r') as f:
            work_config = json.load(f)
        MDL_PATH = work_config['model_path']
        THRESHOLD = work_config['threshold']
        tmp_crop_range = work_config['crop_ranges']
        CROP_RANGES = {
            "x_start": tmp_crop_range['x_start'],
            "x_end": tmp_crop_range['x_end'],
            "y_start": tmp_crop_range['y_start'],
            "y_end": tmp_crop_range['y_end']
        }

        return 

    # 傷ありの結果保存
    def save_defective_info(timestamp, infered_accuracy, image_path, diff_image_path):
        result_json = {
            'timestamp': timestamp,
            'infered_accuracy': float(infered_accuracy),
            'image_path': image_path,
            'diff_image_path': diff_image_path
        }
        json_filename = f'result_{timestamp}.json'
        json_path = os.path.join('results', 'json', json_filename)
        with open(json_path, 'w') as json_file:
            json.dump(result_json, json_file, indent=4)

    # 撮影、回転処理
    def getPctr_and_rotate(cmr, tmp_serial_data):
        global captured_image
        # ---撮影、前処理---
        # 画像を取得
        captured_image = cmr.get_frame()
        if captured_image is None:
            print("!ERR! 画像の取得に失敗しました。")
            return None
        # ---回転命令送信---
        tmp_serial_data.send(PLC_SND_CMD["ROTATE"] + bytes([ROTATE_DEGREE]))
        # PLCから回転完了の信号を受信
        """
        while True:
            data = plc.get_data()
            if data == "ROTATED":
                break
            # 本当は回転済み信号を受け取るまで待つ
            time.sleep(0.1)
        """
        return captured_image

    # 推論処理
    def inference(img_dtrmn: ImgDtrmn_Lib.ImgDtrmn_Lib, inpt_img: np.ndarray):
        global infered_accuracy, infered_image
        try:
            # ---推論処理---
            mse, infered_img = img_dtrmn.inference(inpt_img)
            infered_accuracy = mse
            infered_image = infered_img
            return mse
        except Exception as e:
            print(f"!ERR! 推論中にエラーが発生しました: {e}")
            infered_image = None  # エラー時は推論画像をNoneに設定
            return None


    # メイン関数
    def run(self, serial_data, stop_event: threading.Event):
        global init_image, infered_image
        print("#########################################")
        print("      外観判別システム  Prometheus       ")
        print("                                  ver.1.0")
        print("#########################################")
        print("")
        print("[CMT] プログラムを開始します。")
        
        # 設定ファイルの読み込み
        print("-----------------------------------------")
        print("[CMT] 設定ファイルを読み込みます。")
        self.load_config()
        print("[CMT] 設定ファイルの読み込みが完了しました。")
        print(f"  [CMT] ワーク名: {WORK_NAME}")
        print(f"  [CMT] 回転角度: {ROTATE_DEGREE}")
        print(f"  [CMT] 回転回数: {ROTATE_COUNT}")
        print(f"  [CMT] モデルパス: {MDL_PATH}")
        print(f"  [CMT] 判別閾値: {THRESHOLD}") 
        print(f"  [CMT] クロップ範囲:")
        print (f"    [CMT] X: {CROP_RANGES["x_start"]} to {CROP_RANGES["x_end"]}")
        print (f"    [CMT] Y: {CROP_RANGES["y_start"]} to {CROP_RANGES["y_end"]}")
        # 初期化
        print("-----------------------------------------")
        print("[CMT] 初期化を行います。")

        """
        # SQLサーバーの初期化
        print("  [CMT] SQL通信の初期化を行います。")
        sql_comm = SQLComm.SQLCommunication()
        sql_comm.set_db_name(DB_NAME)
        print("  [CMT] SQL通信の初期化が完了しました。")
        """

        # 外部デバイスの初期化
        print("  [CMT] 外部デバイスの初期化を行います。")

        # カメラの初期化
        print("    [CMT] カメラの初期化を行います...", end="")
        cmr = Cmr_Lib.Cmr_Lib(camera_num=COM_CMR)
        cmr.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)  # 幅を2592pxに設定
        cmr.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944) # 高さを1944pxに設定
        cmr.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))  # 未圧縮形式に設定を試みる
        print("---[OK]")

        """
        # PLCの初期化
        print("    [CMT] PLCの初期化を行います...", end="")
        # SerialCommunicate.jsonから設定を読み込む
        with open("SerialCommunicate.json", "r") as f:
            serial_setting = json.load(f)
        serial_setting = {
            "port": serial_setting["port"],
            "baudrate": serial_setting["baudrate"],
            "parity": serial_setting["parity"],
            "stopbits": serial_setting["stopbits"],
            "timeout": serial_setting["timeout"]
        }
        ##### 一時的な回避
        serial_setting["parity"] = serial.PARITY_NONE   # パリティビットなし 一時的な回避
        serial_setting["stopbits"] = serial.STOPBITS_ONE    # ストップビット1 一時的な回避
        serial_comm = PLC_Lib.SerialCommunicator(**serial_setting)
        plc = PCManager(serial_comm)
        print("---[OK]")
        """

        # 初期状態の背景画像を取得
        print("  [CMT] 初期状態の背景画像を取得します...")
        time.sleep(1)  # カメラの安定化のため待機
        init_image = cmr.get_frame()
        if init_image is None:
            print("!ERR! 初期状態の背景画像の取得に失敗しました。")
            cmr.release()   # カメラの解放
            #plc.release()  # PLCとの通信の解放
            exit()
        print("  [CMT] 背景画像の取得が完了しました。")

        # 変数の初期化
        print("  [CMT] 変数の初期化を行います。")
        is_exist = False    # 存在判定
        print("  [CMT] 変数の初期化が完了しました。")
        print("[CMT] 初期化が完了しました。")

        # モデルのロード
        print("-----------------------------------------")
        print("[CMT] 画像処理システムの初期化を行います。")
        img_dtrmn = ImgDtrmn_Lib.ImgDtrmn_Lib(model_path=MDL_PATH, crop_ranges=CROP_RANGES)
        # モデルのロード
        print("  [CMT] モデルのロードを行います...", end="")
        img_dtrmn.load_model()
        print("---[OK]")
        print("  [CMT] モデルのロードが完了しました。")
        print("  [CMT] 対象モデルの詳細:")
        print(f"          モデル名: {img_dtrmn.model_name}")
        print(f"          ファイル名: {MDL_PATH}")
        print(f"          入力サイズ: {img_dtrmn.input_shape}")
        print(f"          出力サイズ: {img_dtrmn.output_shape}")
        print("[CMT] モデルのロードが完了しました。")
        
        # 結果保存用のディレクトリを作成
        result_dir = 'results'
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        defective_images_dir = os.path.join(result_dir, 'defective_images')
        if not os.path.exists(defective_images_dir):
            os.makedirs(defective_images_dir)
        diff_images_dir = os.path.join(result_dir, 'diff_images')
        if not os.path.exists(diff_images_dir):
            os.makedirs(diff_images_dir)
        json_dir = os.path.join(result_dir, 'json')
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)

        # メインループ
        try:
            while True:
                # PLCからの動作開始を待つ
                data, flag = serial_data.get_receive_data()
                if data == PLC_RCV_CMD["CHECK_EXIST"]:
                    print("*DBG* PLCからの存在確認要求を受信しました。")
                    # 現在の画像を取得
                    current_image = cmr.get_frame()
                    if current_image is None:
                        print("!ERR! 画像の取得に失敗しました。")
                        continue

                    # 存在判定を行う
                    is_exist = cmr.detect_exist(current_image, init_image)
                    if is_exist:
                        serial_data.send(PLC_SND_CMD["EXIST"])  # 存在している場合、PLCにOKを送信
                    else:
                        serial_data.send(PLC_SND_CMD["NOT EXIST"])  # 存在していない場合、PLCにNGを送信
                        #continue   # 次のループへ
                    print("*DBG* 存在判定結果: {is_exist}")

                    # PLCからの動作開始を待つ
                    while True:
                        data, flag = serial_data.get_receive_data()
                        if data == PLC_RCV_CMD["SET WORK"]:
                            print("*DBG* PLCからの作業開始要求を受信しました。")
                            break
                        time.sleep(0.1)

                    ##### 判別処理 #####
                    flg_judge = JUDGE["OK"]  # 判定結果
                    for i in range(ROTATE_COUNT):   # 回転回数分、推論処理を行う
                        print(f"*DBG* {i+1}回目の判別処理を行います。")
                        # 画像取得と回転
                        captured_image = self.getPctr_and_rotate(cmr, serial_data)
                        print("*DBG* 画像取得と回転が完了しました。")
                        # 前処理
                        preprocessed_img = img_dtrmn.pre_processing(captured_image)
                        print("*DBG* 前処理が完了しました。")
                        print(f"前処理後の画像形状: {preprocessed_img.shape}")
                        # 推論
                        mse = self.inference(img_dtrmn, preprocessed_img)
                        print(f"*DBG* 推論結果: {mse}")
                        if mse > THRESHOLD:    # 判定閾値を超えた場合、不良を検出
                            flg_judge = JUDGE["NG"]  # 不良を検出
                            # 結果を保存
                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                            image_filename = f'defective_{timestamp}.png'
                            image_path = os.path.join(defective_images_dir, image_filename)
                            # 元の画像を保存
                            cv2.imwrite(image_path, captured_image)
                            print(f"*DBG* 不良画像を保存しました: {image_path}")
                            # 差分画像を生成して傷をマーク
                            scaled_img = img_dtrmn.robust_scale_image(infered_image)# infered_imageを二次元化して、差分画像を生成
                            print("*DBG* 推論画像を二次元化しました。")
                            diff_image = img_dtrmn.mark_defects(preprocessed_img, scaled_img)
                            print("*DBG* 差分画像を生成しました。")
                            diff_image_filename = f'diff_{timestamp}.jpg'
                            diff_image_path = os.path.join(diff_images_dir, diff_image_filename)
                            cv2.imwrite(diff_image_path, diff_image)
                            print(f"*DBG* 差分画像を保存しました: {diff_image_path}")
                            # JSONファイルを作成
                            self.save_defective_info(timestamp, infered_accuracy, image_path, diff_image_path)
                            break  # 不良を検出したらループを抜ける

                    # 判別結果送信
                    print("*DBG* 判別結果: {flg_judge}")
                    if flg_judge == JUDGE["OK"]:
                        serial_data.send(PLC_SND_CMD["FLAWLESS"])
                        # 良品をカウントアップ  SQLiteに保存
                    else:
                        serial_data.send(PLC_SND_CMD["DEFECTIVE"])
                        # 不良品をカウントアップ SQLiteに保存
                    ##### 判別処理 #####

                # threadの停止判断
                if self.stop_event.is_set():
                    print("[CMT] プログラムを終了します。")
                    break
                
                time.sleep(0.1)  # CPU負荷を下げるためにスリープ

        except Exception as e:
            # 異常終了
            print("!ERR! プログラムを異常終了します。")
            print(f"!ERR! エラー内容: {e}")
        except KeyboardInterrupt:
            # Ctrl+Cで終了
            print("[CMT] プログラムを終了します。")
        finally:
            # リソースの解放
            cmr.release()
            #plc.release()

if __name__ == '__main__':
    stop_event = threading.Event()
    # SerialCommunicate.jsonから設定を読み込む
    with open("SerialCommunicate.json", "r") as f:
        serial_setting = json.load(f)
    serial_setting = {
        "port": serial_setting["port"],
        "baudrate": serial_setting["baudrate"],
        "parity": serial_setting["parity"],
        "stopbits": serial_setting["stopbits"],
        "timeout": serial_setting["timeout"]
    }
    ##### 一時的な回避
    serial_setting["parity"] = serial.PARITY_NONE   # パリティビットなし 一時的な回避
    serial_setting["stopbits"] = serial.STOPBITS_ONE    # ストップビット1 一時的な回避
    serial_data = serial_gate.SerialGate(serial_setting, stop_event)
    prometheus = Prometheus(stop_event)
    prometheus.run(serial_data, stop_event)
    stop_event.set()
    print("[CMT] プログラムを終了します。")
    exit()