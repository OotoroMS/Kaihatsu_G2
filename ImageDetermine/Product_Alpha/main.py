# メインプログラム

# ライブラリのインポート
import numpy as np
import cv2
import tensorflow as tf
import threading
import time
import json
import os
from datetime import datetime  # 追加

# 自作ライブラリのインポート
import ImageDetermine.Product_Alpha.ImgDtrmn_Lib as ImgDtrmn_Lib
import ImageDetermine.Product_Alpha.Cmr_Lib as Cmr_Lib
import ImageDetermine.Product_Alpha.PLC_Lib as PLC_Lib

# グローバル変数
COM_PLC = "COM1"        # PLCのCOMポート
COM_CMR = 0             # カメラのデバイス番号（デフォルトカメラを使用）

# 変数の初期化（後で設定ファイルから読み込む）
MDL_PATH = ""           # モデルのパス
ROTATE_DEGREE = 0       # 回転角度
ROTATE_COUNT = 0        # 回転回数

JUDGE = {               # 判定結果
    "OK": True,
    "NG": False,
}

PLC_SND_CMD = {         # PLC送信コマンド
    "OK": "OK",
    "NG": "NG",
}

THRESHOLD = 0.003        # 判別閾値

captured_image = None   # 撮影した画像
infered_accuracy = 0    # 推論結果
infered_image = None    # 推論画像
init_image = None       # 初期状態の背景画像

# 設定ファイルの読み込み
def load_config():
    global MDL_PATH, ROTATE_DEGREE, ROTATE_COUNT, THRESHOLD
    # determine_config.jsonを読み込む
    with open('determine_config.json', 'r') as f:
        config = json.load(f)

    work_name = config.get('work_name')
    ROTATE_DEGREE = config.get('rotate_degree')
    ROTATE_COUNT = config.get('rotate_count')
    model_config_file = config.get('model_config_file')

    # モデル設定ファイルを読み込む
    with open(model_config_file, 'r') as f:
        model_config = json.load(f)

    model_name = model_config.get('model_name')
    work_name_model = model_config.get('work_name')
    crop_ranges = model_config.get('crop_ranges')

    # モデルのパスを設定
    MDL_PATH = os.path.join('models', work_name_model, model_name + '.h5')

    # THRESHOLDをモデルごとに設定（必要に応じて設定ファイルに追加）
    # ここでは仮に設定
    THRESHOLD = 0.003

    return crop_ranges

# 撮影、回転処理
def getPctr_and_rotate(cmr, plc):
    global captured_image
    # ---撮影、前処理---
    # 画像を取得
    captured_image = cmr.get_frame()
    if captured_image is None:
        print("!ERR! 画像の取得に失敗しました。")
        return False
    # 必要に応じて前処理をここで行う
    # ---回転命令送信---
    plc.send_data("ROTATE")
    # PLCから回転完了の信号を受信
    while True:
        data = plc.get_data()
        if data == "ROTATED":
            break
        time.sleep(0.1)
    return True

# 推論処理
def inference(img_dtrmn, inpt_img):
    global infered_accuracy, infered_image
    # ---推論処理---
    mse, infered_img = img_dtrmn.inference(inpt_img)
    infered_accuracy = mse
    infered_image = infered_img
    return mse

# メイン関数
def main():
    global init_image  # 初期状態の背景画像
    print("#########################################")
    print("      外観判別システム  Prometheus       ")
    print("                                  ver.1.0")
    print("#########################################")
    print("")
    print("[CMT] プログラムを開始します。")
    
    # 設定ファイルの読み込み
    print("-----------------------------------------")
    print("[CMT] 設定ファイルを読み込みます。")
    crop_ranges = load_config()
    print("[CMT] 設定ファイルの読み込みが完了しました。")
    print(f"  [CMT] ワーク名: {crop_ranges.get('work_name')}")
    print(f"  [CMT] 回転角度: {ROTATE_DEGREE}")
    print(f"  [CMT] 回転回数: {ROTATE_COUNT}")
    print(f"  [CMT] モデルパス: {MDL_PATH}")
    print(f"  [CMT] クロップ範囲: {crop_ranges}")

    # 初期化
    print("-----------------------------------------")
    print("[CMT] 初期化を行います。")
    # 外部デバイスの初期化
    print("  [CMT] 外部デバイスの初期化を行います。")
    # カメラの初期化
    print("    [CMT] カメラの初期化を行います...", end="")
    cmr = Cmr_Lib.Cmr_Lib(camera_num=COM_CMR)
    print("---[OK]")
    # PLCの初期化
    print("    [CMT] PLCの初期化を行います...", end="")
    plc = PLC_Lib.PLC_Lib(port=COM_PLC)
    print("---[OK]")
    # 初期状態の背景画像を取得
    print("  [CMT] 初期状態の背景画像を取得します...")
    time.sleep(1)  # カメラの安定化のため待機
    init_image = cmr.get_frame()
    if init_image is None:
        print("!ERR! 初期状態の背景画像の取得に失敗しました。")
        cmr.release()
        plc.release()
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
    img_dtrmn = ImgDtrmn_Lib.ImgDtrmn_Lib(model_path=MDL_PATH, crop_ranges=crop_ranges)
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
    json_dir = os.path.join(result_dir, 'json')
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    # メインループ
    try:
        while True:
            # PLCからの動作開始を待つ
            data = plc.get_data()
            if data == PLC_Lib.STATE["START"]:
                # 現在の画像を取得
                current_image = cmr.get_frame()
                if current_image is None:
                    print("!ERR! 画像の取得に失敗しました。")
                    continue

                # 存在判定を行う
                is_exist = cmr.detect_exist(current_image, init_image)
                if is_exist:
                    plc.send_data(PLC_SND_CMD["OK"])  # 存在している場合、PLCにOKを送信
                else:
                    plc.send_data(PLC_SND_CMD["NG"])  # 存在していない場合、PLCにNGを送信
                    continue   # 次のループへ

                ##### 判別処理 #####
                flg_judge = JUDGE["OK"]  # 判定結果
                for i in range(ROTATE_COUNT):   # 回転回数分、推論処理を行う
                    # 画像取得と回転
                    getPctr_and_rotate(cmr, plc)
                    # 前処理
                    preprocessed_img = img_dtrmn.pre_processing(captured_image)
                    # 推論
                    mse = inference(img_dtrmn, preprocessed_img)
                    if infered_accuracy > THRESHOLD:    # 判定閾値を超えた場合、不良を検出
                        flg_judge = JUDGE["NG"]  # 不良を検出
                        # 結果を保存
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                        image_filename = f'defective_{timestamp}.png'
                        image_path = os.path.join(defective_images_dir, image_filename)
                        # 元の画像を保存
                        cv2.imwrite(image_path, captured_image)
                        # 差分画像を生成して傷をマーク
                        diff_image = img_dtrmn.mark_defects(preprocessed_img, infered_image)
                        diff_image_filename = f'defective_diff_{timestamp}.png'
                        diff_image_path = os.path.join(defective_images_dir, diff_image_filename)
                        cv2.imwrite(diff_image_path, diff_image)
                        # JSONファイルを作成
                        result_json = {
                            'timestamp': timestamp,
                            'infered_accuracy': infered_accuracy,
                            'image_path': image_path,
                            'diff_image_path': diff_image_path
                        }
                        json_filename = f'result_{timestamp}.json'
                        json_path = os.path.join(json_dir, json_filename)
                        with open(json_path, 'w') as json_file:
                            json.dump(result_json, json_file, indent=4)
                        break  # 不良を検出したらループを抜ける

                # 判別結果送信
                if flg_judge == JUDGE["OK"]:
                    plc.send_data(PLC_SND_CMD["OK"])
                else:
                    plc.send_data(PLC_SND_CMD["NG"])
                ##### 判別処理 #####

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
        plc.release()

if __name__ == "__main__":
    main()
