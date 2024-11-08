#外観検査表示(外観検査に修正する予定)
import pygame
import os
import Graph
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture
from pathlib import Path
import shutil #ディレクトリ削除用
from PIL import Image
import glob

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
PATH = "GUI_option_test\\image\\graph.png"

class GraphFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.create_flg = True
        self.buttons = {
            Button(self.screen, 0, 960, 330, 120, "GUI_option_test\\image\\button\\back.png", self.move_data)
        }
        self.images = [
            Picture(self.screen, 0, 0, 750, 200, "GUI_option_test\\image\\title\\pic18.png"),
            Picture(self.screen, 310, 200, 1300, 740, "GUI_option_test\\image\\exptxt\\pic77.png")
        ]
    
    #   画面描画処理
    def draw(self):
        self.draw_graph()
        for image in self.images:
            image.draw()
        #self.screen.blit(self.graph, (270,190))
        for button in self.buttons:
            button.draw()
    
    #   グラフ描画・更新処理
    def draw_graph(self):
        self.delete_old_images("GUI_option_test\\image\\sample")
        dir_path = Path("GUI_option_test\\image\\sample")
        files = list(dir_path.glob("*.jpg"))
        print(len(files))

        if len(files) > 12:#ファイルが多くなると一旦削除してから作り直す、
            path = "GUI_option_test\\image\\sample"
            shutil.rmtree(path)
            os.mkdir(path)
        elif len(files) > 0:
            list_date=[]
            for i in range(len(files)):
                file_name, ext = os.path.splitext(files[i].name)
                list_date.append(file_name)
            print(list_date)

            list_date_sort=sorted(list_date,reverse=True)
            self.list_date_new=list_date_sort[0]
            print(self.list_date_new)
            #img1=Image.open("D:/GitHub/Kaihatsu_G2/UI試作/テスト用_画像/"f"/{list_date_new}.jpg")
            self.images[1] = Picture(self.screen, 290, 200, 1300, 740, "GUI_option_test\\image\\sample\\"f"\\{self.list_date_new}.jpg")
            
        else:
            print("NO_image")
            self.images[1] = Picture(self.screen, 290, 200, 1300, 740, "GUI_option_test\\image\\exptxt\\pic77.png")

    #   データ一覧画面に遷移
    def move_data(self):
        self.create_flg = True
        return "data"
    
    def delete_old_images(self,directory_path):
        # 指定されたディレクトリ内のすべての画像ファイルを取得（jpg, png）
        image_files = glob.glob(os.path.join(directory_path, "*.[jp][pn]g"))
        
        if not image_files:
            print("画像ファイルが見つかりませんでした。")
            return
        
        # 画像ファイルを最終更新日時でソート（新しい順）
        image_files.sort(key=os.path.getmtime, reverse=True)
        
        # 一番新しい画像ファイルを除く他の画像を削除
        for file_to_delete in image_files[1:]:
            try:
                os.remove(file_to_delete)
                print(f"{file_to_delete} を削除しました。")
            except Exception as e:
                print(f"{file_to_delete} の削除中にエラーが発生しました: {e}")