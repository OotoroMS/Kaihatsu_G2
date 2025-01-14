#外観検査
import pygame
import shutil #ディレクトリ削除用
import glob
import os
from pathlib import Path

# 定数
from GUI.constant.file_path                 import *
from GUI.constant.color                     import *
from GUI.constant.judge_result              import *
from GUI.constant.screen.screen_name        import *
from GUI.constant.screen.vision_constant    import *
# 部品
from GUI.parts.Button   import Button
from GUI.parts.Picture  import Picture
# 基礎クラス
from GUI.screen.BaseScreen import BaseScreen

class VisionScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
    
    # ボタンの宣言
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_BACK_STATUS, func=self.back)
        ]

    # 画像の設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **TITLE_VISION_STATUS),
            Picture(self.screen, **EXPTXT_NO_IMAGE_STATUS)
        ]

    def draw(self):
        self.update_vision()
        super().draw()

    def update_vision(self):
        self.delete_old_images()
        # 画像読み込み
        dir_path = Path(SUMPLE_FILE_PATH)
        files    = list(dir_path.glob("*.jpg"))
        # 画像が存在すれば
        if len(files) > ZERO:
            image_path = files[0]
            self.images[1] = Picture(self.screen, EXPTXT_NO_IMAGE_STATUS["coordinate"], EXPTXT_NO_IMAGE_STATUS["size"], f"{image_path}")
        else:
             self.images[1] = Picture(self.screen, **EXPTXT_NO_IMAGE_STATUS)
        

    # 古い画像を削除
    def delete_old_images(self):
        # 画像を取得
        image_files = glob.glob(os.path.join(SUMPLE_FILE_PATH, "*.[jp][pn]g"))
        if image_files:
            self.delete_images(image_files)
        
    def delete_images(self, files : list[str]):
        # 新しい順にソート
        files.sort(key=os.path.getatime, reverse=True)
        # 最も新しい画像を残して削除
        for file in files[1:]:
            try:
                os.remove(file)
            except Exception as e:
                print(f"エラーが発生しました: {e}")
    
    # 前の画面に戻る
    def back(self):
        return DATA, SUCCESS
