#カウントの表を表示する設定
import pygame
import GUI.parts.CountList as CountList

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
TODAY = ["日付", "総個数", "良品", "不良品"]
SEVEN = ["日付", "総個数", "良品", "不良品"]
ERROR = ["番号", "日付"]

#   表を描画
def draw_table(screen ,view, bad_view, font):
    table, get_data = CountList.create_table(view)
    list = convert_list(view, get_data)
    for i in range(0, len(table), 1):
        draw_table_rect(screen,table[i])
        set_table_data(view,screen, table[i], list, i, bad_view, font)
    if view == "error":
        return len(list)
    else:
        return 0

#   配列の次元を落とす
def convert_list(view, base_list):
    result_list = list()
    for data in base_list:
        for set_data in data:
            result_list.append(set_data)
    return result_list

#   表の枠を描画
def draw_table_rect(screen ,table):
    pygame.draw.rect(screen, GRAY, table)
    pygame.draw.rect(screen, BLACK, table,1)

#   表示内容に合わせて、作成した表の枠にヘッダとデータを描画
def set_table_data(view, screen, table, data_list, index, bad_view, font):
    if view == "error" and index <= 1:
        seting_text(screen, table, ERROR[index], font)
    elif view == "error":
        if len(data_list) > ((index + bad_view) - 2):
            seting_text(screen, table, str(data_list[(index + bad_view) - 2]), font)
    elif view == "today" and index <= 3:
        seting_text(screen, table, TODAY[index], font)
    elif view == "seven" and index <= 3:
        seting_text(screen, table, SEVEN[index], font)
    else:
        if len(data_list) > (index - 4):
            seting_text(screen, table, str(data_list[index - 4]), font)

#   テキスト描画処理
def seting_text(screen, table, text, table_font):
    text_img = table_font.render(text, True, BLACK)
    text_rect = text_img.get_rect(center=table.center)
    screen.blit(text_img,text_rect)