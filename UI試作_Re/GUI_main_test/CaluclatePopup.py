from typing import Tuple, Optional

def calculate_popup_size(base_width : int, base_height : int) -> Tuple[int, int]:
    """
    popup画面のサイズを計算するモジュール。
    縦横ともに、200引いた値を返す。

    Parameters:
    base_width (int) :  基準画面の横幅
    base_height (int) : 基準画面の縦幅
    Returens:
    Tuple[int, int] :   popup画面の横幅及び縦幅
    """
    if base_width and base_height:
        return base_width - 200, base_height - 200

def caluclate_popup_position(base_width : int, base_height : int, popup_width : int, popup_height : int)->Tuple[Optional[int], Optional[int]]:
    """
    popup画面の表示位置を計算する関数。
    画面全体の縦幅と横幅からpopup画面の縦幅と横幅を引いた値を2で割った値を返す。
    popup画面の縦幅及び横幅がなければ(0,0)を返す。

    Parameters:
    base_width (int) :  基準画面の横幅
    base_height (int) : 基準画面の縦幅
    popup_width (int) : popup画面の横幅
    popup_height (int)  : popup画面の縦幅

    Returens:
    Tuple[int, int] :   popup画面の描画開始座標。popup画面の縦幅及び横幅がなければ(0,0)
    """
    if popup_width and popup_height:
        return ((base_width - popup_width)//2 , (base_height - popup_height) // 2)
    else:
        return None, None