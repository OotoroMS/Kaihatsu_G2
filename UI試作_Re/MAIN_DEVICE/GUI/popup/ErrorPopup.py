import pygame
from typing import Tuple, Optional, List
# ベースクラス
from GUI.popup.BasePopup import BasePopup
# 定数
from GUI.constant.file_path  import *
from GUI.constant.popup_name import *
from GUI.constant.color      import *
from GUI.constant.popup_text import *
from GUI.constant.normal     import *
# 部品
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture

ERROR_IMG = {    
    "size"       : (330, 300),
    "image_path" : EXPTXT_FILE_PATH + "error.png"
}

class ErrorPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, text_index: str) -> None:
        super().__init__(screen)
        self.code: str = "エラー002"
        self.location: str = "寸法部"
        self.setting_text(text_index)
        self.view_images()

    # テキストを生成
    def setting_text(self, text_index: str) -> None:
        self.view_texts: List[pygame.Surface] = []  # view_texts の型を明確に指定
        if text_index in POPUP_TEXTS.keys():
            # 表示用テキストを生成
            self.view_texts = [
                self.text_font.render(POPUP_TEXTS[text_index], True, WHITE),
                self.text_font.render(self.code, True, WHITE),
                self.text_font.render(self.location, True, WHITE)
            ]

    def view_images(self, coordinate: Optional[List[int]] = None) -> None:
        if coordinate is None:
            coordinate = self.img_coordinate()
        self.view_img: Picture = Picture(self.screen, coordinate=coordinate, **ERROR_IMG)

    # ボタンの設定
    def setting_buttons(self) -> None:
        button_width: int = self.width // 4
        button_height: int = self.height // 4
        button_x: int = self.pos_x + (self.width // 2) - (button_width // 2)
        button_y: int = self.height - (self.height // 4)
        self.buttons: List[Button] = [
            Button(self.screen, (button_x, button_y), (button_width, button_height), BACK_BOTTON_FILE_PATH, self.close_popup)
        ]

    def draw(self) -> None:
        super().draw()
        self.text_update()
        # 最初のY座標を中央から3行分上に移動
        line_height = self.view_texts[0].get_height()  # 1行分の高さ
        y_offset: int = (self.height // 2) - (line_height // 2) - (line_height * 1)  # 中央から2行分上に設定

        # 3つのテキストを描画
        for text_surface in self.view_texts:
            text_x = self.get_centered_x(text_surface)  # 中央揃えでX座標を計算
            self.screen.blit(text_surface, (text_x, y_offset))  # テキストを描画
            y_offset += text_surface.get_height()  # 次のテキストのY位置を更新

        # 画像の描画
        self.view_img.draw()

    def get_centered_x(self, text_surface: pygame.Surface) -> int:
        text_width: int = text_surface.get_width()
        text_x: int = self.pos_x + (self.width - text_width) // 2  # 中央揃えのX座標
        return text_x


    # 画像を貼る座標の計算
    def img_coordinate(self) -> List[int]:
        # 表示テキストの幅と高さを取得
        text_width: int = self.view_texts[0].get_width()  # 最初のテキストの幅を基準
        text_height: int = self.view_texts[0].get_height()  # 最初のテキストの高さを基準

        # 貼る画像の幅と高さ取得
        img_width, img_height = ERROR_IMG["size"]

        # x座標の計算
        text_center_x: int = self.pos_x + (self.width - text_width) // 2
        img_offset_x: float = img_width * 0.9  # オフセット調整
        img_x: int = text_center_x - int(img_offset_x)

        # y座標の計算                
        img_y: int = self.pos_y + text_height * 2

        return [img_x, img_y]

    # ボタンのイベント処理
    def close_popup(self) -> Tuple[bool, str]:
        return True, OK

    # エラーメッセージの内容を更新
    def error_update(self, error: Tuple[str, str]):
        # エラーコードと場所を更新
        self.code     = error[0]
        self.location = error[1]
    
    # エラーメッセージを更新
    def text_update(self):
        self.view_texts[1] = self.text_font.render(self.code, True, WHITE)
        self.view_texts[2] = self.text_font.render(self.location, True, WHITE)