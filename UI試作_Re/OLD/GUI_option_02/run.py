import pygame
import App

FONT = "C:\\Windows\\Fonts\\msgothic.ttc"

if __name__ == "__main__":
    pygame.init()
    # 試験用
    screen = pygame.display.set_mode((1920,1080))
    app = App.App(screen,FONT)
    app.run()
    pygame.quit()