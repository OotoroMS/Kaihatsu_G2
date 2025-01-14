import pygame

BACKCOLOR = {
    "稼働中"    :   ((0, 255, 0)),
    "停止中"    :   ((255, 255, 0)),
    "エラー"    :   ((255, 0, 0))
}

OPERATIONACTIVE = "稼働中"
OPERATIONSTOPED = "停止中"
OPERATIONERROR = "エラー"

BLACK = ((0,0,0))

def setting_vital(text_vital, font):
    vital = font.render(text_vital, True, BLACK)
    rect = pygame.rect.Rect(1410, 10, 500, 160)
    vital_point = vital.get_rect(center=rect.center)
    return vital, rect, vital_point

def draw_vital(screen, vital, vital_point, rect ,font):
    pygame.draw.rect(screen, BACKCOLOR[vital], rect)   #   稼働状況更新の領域を確保
    pygame.draw.rect(screen, BLACK, rect, 1)        #   外枠を描画
    view_vital = font.render(vital, True, BLACK)
    screen.blit(view_vital, vital_point)

def update_vital(tcnt,vital):
    if tcnt == 60:
        tcnt = 0
        vital = vital_test(vital)
    else:
        tcnt += 1
    return vital, tcnt

def vital_test(vital):
    if vital == OPERATIONACTIVE:
        vital = OPERATIONSTOPED
    elif vital == OPERATIONSTOPED:
        vital = OPERATIONERROR
    else: 
        vital = OPERATIONACTIVE
    return vital