import tkinter as tk

def show_screen_a():
    screen_a.pack()
    screen_b.pack_forget()

def show_screen_b():
    screen_a.pack_forget()
    screen_b.pack()

root = tk.Tk()
root.title("画面切り替え")
root.geometry("250x50")

# スクリーンAのフレーム
screen_a = tk.Frame(root)
screen_a.pack()

label_a = tk.Label(screen_a, text="ScreenA")
label_a.pack()

button_a = tk.Button(screen_a, text="To B", command=show_screen_b)
button_a.pack()

# スクリーンBのフレーム
screen_b = tk.Frame(root)
screen_b.pack()

label_b = tk.Label(screen_b, text="ScreenB")
label_b.pack()

button_b = tk.Button(screen_b, text="To A", command=show_screen_a)
button_b.pack()

# 最初はスクリーンAを表示
show_screen_a()

root.mainloop()