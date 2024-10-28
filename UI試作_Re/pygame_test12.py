#謎の立方体回転
import pygame
import sys
import math

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rotating Cube Transition")

# 色の定義 (RGB形式)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# 立方体の頂点と面
cube_vertices = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),  # 前面
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)      # 背面
]

cube_faces = [
    (0, 1, 2, 3),  # 前面
    (4, 5, 6, 7),  # 背面
    (0, 1, 5, 4),  # 左面
    (2, 3, 7, 6),  # 右面
    (0, 3, 7, 4),  # 上面
    (1, 2, 6, 5)   # 下面
]

# 回転行列
def rotate_point(point, angle_x, angle_y):
    # 回転行列を使用して3D空間で回転させる
    x, y, z = point
    # X軸回転
    temp_y = y * math.cos(angle_x) - z * math.sin(angle_x)
    temp_z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y = temp_y
    z = temp_z
    # Y軸回転
    temp_x = x * math.cos(angle_y) + z * math.sin(angle_y)
    temp_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x = temp_x
    z = temp_z
    return x, y, z

# 立方体を描画する関数
def draw_cube(angle_x, angle_y):
    projected_vertices = []
    for vertex in cube_vertices:
        rotated_vertex = rotate_point(vertex, angle_x, angle_y)
        # 投影変換 (2D座標に変換)
        f = 200 / (200 + rotated_vertex[2])  # 遠近法
        x = int(rotated_vertex[0] * f * 100 + screen_width / 2)
        y = int(rotated_vertex[1] * f * 100 + screen_height / 2)
        projected_vertices.append((x, y))
    
    # 面を描画
    for face in cube_faces:
        polygon = [projected_vertices[i] for i in face]
        pygame.draw.polygon(screen, WHITE, polygon, 1)  # 面の枠を描画

# メインループ
running = True
angle_x, angle_y = 0, 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLUE)  # 背景を青に塗りつぶす

    # 回転を更新
    angle_x += 0.01
    angle_y += 0.01

    # 立方体を描画
    draw_cube(angle_x, angle_y)

    # 描画を更新
    pygame.display.flip()
    pygame.time.delay(30)  # フレームレート調整

pygame.quit()
sys.exit()
