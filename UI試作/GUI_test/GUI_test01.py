#必要ライブラリのインポート
from pathlib import Path
import os.path
dir_path=Path("真鍮_白黒画像")
#ファイルリストの作成
gettxt=dir_path.glob("*.jpg")
files=list(dir_path.glob("*.jpg"))
#フォルダに格納されているExcelファイルの名前をリスト化
list_date=[]
for i in range(len(files)):
        file_name, ext = os.path.splitext(files[i].name)
        #タイトルに"Book1"がない場合はリストに入れない
        if "20240712" not in file_name:
            continue
        list_date.append(file_name)
#print(list_date)
#日付順の新しいソートし、要素０番目に指定
list_date_new=sorted(files,reverse=True)[0]

#print("%s" %(list_date_new[0]))
print("真鍮_白黒画像\\"+[list_date_new.stem for list_date_new in files][0]+".jpg")

