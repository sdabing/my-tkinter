# -*- coding:utf-8 -*-
from Tkinter import *

class Red():

    def __init__(self, root, btn, label):
        self.label = label
        self.btn = btn
        self.root = root
        self.n = 0

    def gs(self):
        self.btn['command'] = self.cc

    def cc(self):
        if self.n == 0:
            self.label['bg'] = 'red'
        if self.n == 1:
            self.label['bg'] = 'yellow'
        if self.n == 2:
            self.label['bg'] = 'blue'
        self.n += 1
        if self.n >= 3:
            self.n = 0
        self.root.after(1000, self.cc)

if __name__ == '__main__':
    root = Tk()
    btn = Button(root, text='开始游戏')
    label = Label(root, text='颜色')
    r = Red(root, btn, label)
    r.gs()
    label.pack()
    btn.pack()
    root.mainloop()
