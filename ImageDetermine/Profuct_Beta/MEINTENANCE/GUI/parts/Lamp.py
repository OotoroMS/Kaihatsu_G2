#動作確認のランプ
import pygame
from typing import Tuple, Optional
from MEINTENANCE.GUI.constants.color    import *


# 赤の円（塗りつぶし）
# pygame.draw.circle(描画画面, 色(塗り潰し), 中心座標, 半径)
# 四角形
# pygame.draw.rect(描画画面, 色(塗り潰し), 図形の形(左上のx,y,横幅,立幅),線の幅)
# 線の太さ指定
# pygame.draw.circle(screen, (255,0,0), (320,240), 100, 5)


class Lamp():
    
    def __init__(self, screen : pygame.Surface, x : int, y : int, w : int, h : int, color : Tuple[int, int, int]) -> None:
        """
        矩形の描画処理を管理するクラス。
        動作確認画面で、各機構の動作状況を表示するランプとして使用する。

        Prameters:
        screen (Surface)    :   描画する画面
        x (int) :   左上のx座標
        y (int) :   左上のy座標
        w (int) :   横幅
        h (int) :   立幅
        color (Tuple[int, int, int]) :  塗りつぶす色（RGB）
        """
        self.screen = screen
        self.rect_status = (x, y, w, h)
        self.color = color
    
    def draw(self) -> None:
        """
        矩形を描画する関数。
        画面更新時に実行する。
        """
        pygame.draw.rect(self.screen, self.color, self.rect_status, 0)
        # print("lamp draw")

    def confirmation_color(self, color : Tuple[int,int,int]) -> bool:
        """
        色の範囲が指定値以内に収まっているか確認するモジュール。
        引数で渡された値の範囲が0～255の間に収まっているときはTrue,
        収まっていないときはFalseを返す。

        Parameters:
        color (Tuple[int, int, int]) : 変更する色(RGB)
        """
        print("color  :",color)
        print("sample :", GREEN)
        for color_rgb in color:
            if color_rgb < 0 or color_rgb > 255:
                print("not update")
                return False
            print("color_rgb :", color_rgb)
        
        return True
    
    def update_color(self, color) -> None:
        """
        矩形を塗りつぶす色を更新するモジュール。
        色が規定の範囲内のときのみ更新する。
        
        Parameters:
        color (Tuple[int, int, int]) : 変更する色(RGB)
        """
        # if self.confirmation_color(color):
        self.color = color
        # print("color update")
        # print(self.color)

    def update_rect(self, x, y, w, h):
        self.rect_status = (x, y, w, h)
