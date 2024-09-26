from tkinter import *
from tkinter import ttk

mainform = Tk()
mainform.title('test')

frame1 = ttk.Frame(mainform,padding=200)
label1 = ttk.Label(frame1,text='テキストを入力してください')
t = StringVar()
entry1 = ttk.Entry(frame1,textvariable=t)
button1 = ttk.Button(
    frame1,
    text='OK',
    command=lambda: print('入力値は,%s' % t.get())
)

frame1.pack()
label1.pack(side=LEFT)
entry1.pack(side=LEFT)
button1.pack(side=LEFT)

mainform.mainloop()
