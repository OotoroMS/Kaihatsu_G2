#画面遷移の際、暗転させるプログラム
import pygame

#   暗転用
DARK_COLOR = (0,0,0)
DARKEN_DURATION = 3  # 暗くするフレーム数

#   暗転処理
def brackout_screen(screen, image, draw_func):
    overlay = _create_overlay()                     #   暗転用のオーバーレイを生成

    for frame in range(DARKEN_DURATION):
        darken_alpha = 255 * frame // DARKEN_DURATION
        _brackout(screen,image,frame, overlay, draw_func)
        _update_screen(30)

#   明転処理
def lightchenge_screen(screen, image, draw_func):
    #   オーバーレイ生成
    overlay = _create_overlay()
    #   暗いオーバーレイを消す
    _erase_overlay(screen, overlay)
    #   明転
    for frame in range(DARKEN_DURATION):
        _lightchenge(screen,image, frame, overlay, draw_func)
        _update_screen(30)

#   オーバーレイを生成        
def _create_overlay():
    w, h = pygame.display.get_surface().get_size()      #   画面サイズを取得
    overlay = pygame.Surface((w,h))
    overlay.fill(DARK_COLOR)
    return overlay

#   暗いオーバーレイを消す
def _erase_overlay(screen, overlay):
    overlay.set_alpha(255)
    screen.blit(overlay, (0, 0))
    _update_screen(100)

#   暗転
def _brackout(screen, image, frame, overlay, draw_func):
    darken_alpha = 255 * frame // DARKEN_DURATION
    overlay.set_alpha(darken_alpha)
    screen.blit(image, (0, 0))
    draw_func()
    screen.blit(overlay, (0, 0))

#   明転
def _lightchenge(screen, image, frame, overlay, draw_func):
    overlay.set_alpha(255 - (255 * frame // DARKEN_DURATION))
    screen.blit(image, (0, 0))
    draw_func()
    screen.blit(overlay, (0,0))

#   画面更新処理
def _update_screen(time):
    pygame.display.flip()
    pygame.time.delay(time)