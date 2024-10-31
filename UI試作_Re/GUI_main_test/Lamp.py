import pygame
from typing import Tuple, Optional
YEROW = ((255,255,0))
GREEN = ((0,255,0))
RED   = ((255,0,0))

# 赤の円（塗りつぶし）
# pygame.draw.circle(描画画面, 色(塗り潰し), 中心座標, 半径)
# 線の太さ指定
# pygame.draw.circle(screen, (255,0,0), (320,240), 100, 5)


class Lamp():
    #   必要に応じて半径も引数に入れたほうがいいと思われる
    def __init__(self, screen : pygame.Surface, x : int, y : int, color : Tuple[int, int, int]) -> None:
        """
        円の描画処理を管理するクラス。
        動作確認画面で、各機構の動作状況を表示するランプとして使用する。

        Prameters:
        screen (Surface)    :   描画する画面
        x (int) :   中心のx座標
        y (int) :   中心のy座標
        color (Tuple[int, int, int]) :   円を塗りつぶす色（RGB）
        """
        self.screen = screen
        self.coordinate = (x, y)
        self.color = color
    

    def draw(self) -> None:
        """
        円を描画する関数。
        画面更新時に実行する。
        """
        pygame.draw.circle(self.screen, self.color, self.coordinate, 10)

    def confirmation_color(self, color : Tuple[int,int,int]) -> bool:
        """
        色の範囲が指定値以内に収まっているか確認するモジュール。
        引数で渡された値の範囲が0～255の間に収まっているときはTrue,
        収まっていないときはFalseを返す。

        Parameters:
        color (Tuple[int, int, int]) : 変更する色(RGB)
        """
        for color_rgb in color:
            if color_rgb < 0 or color_rgb > 255:
                print("not update")
                return False
        
        return True
    
    def update_color(self, color) -> None:
        """
        円を塗りつぶす色を更新するモジュール。
        色が規定の範囲内のときのみ更新する。
        
        Parameters:
        color (Tuple[int, int, int]) : 変更する色(RGB)
        """
        if self.confirmation_color(color):
            self.color = color
                



