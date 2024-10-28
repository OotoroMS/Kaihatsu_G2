#マウス追従_font調査
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.Font("box_01/NotoSerifJP-VariableFont_wght.ttf", 20)    
text_image = font.render("こんにちは, pygame", True, pygame.Color("green"))
pic_image = pygame.image.load("box_01/pin_red.png").convert()

while True:
    pygame.event.clear()
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_ESCAPE]:
        break
    
    test01 = pygame.mouse.get_pos()#位置取得
    screen.fill(pygame.Color("black"))
    screen.blit(pic_image, (test01[0]-70,test01[1]-75))#xyに分けて位置微調節
    screen.blit(text_image, (test01[0]-1,test01[1]-75))#xyに分けて位置微調節
    pygame.display.update()

pygame.quit()