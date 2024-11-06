import sys
import pygame


def main():
    # pygameの初期化
    pygame.init()
    # メイン画面（Surface）初期化(横, 縦)
    main_surface = pygame.display.set_mode((300, 300)) 
    # メイン画面のタイトル
    pygame.display.set_caption("Pygame Sample 2")
    # Clockオブジェクトの生成
    clock = pygame.time.Clock()
    
    #ボールのy座標
    y = 0
    # ループを続けるかのフラグ
    going = True
    # 終了イベント発生までループをまわす
    while going:
        # イベントを取得
        for event in pygame.event.get():
            # 終了イベント（画面の×ボタン押下など）の場合、
            # ループを抜ける
            if event.type == pygame.QUIT:
                going = False
 
        # メイン画面の初期化
        main_surface.fill((220, 220, 220))
        # ボールの座標を更新
        y += 3
        # ボールの描画
        pygame.draw.circle(main_surface, (255,0,0), (150, y), 20)
        # メイン画面の更新
        pygame.display.update()

        # フレームレート（1秒間に何回画面を更新するか）の設定
        clock.tick(10)

    # 終了処理
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()