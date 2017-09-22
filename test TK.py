# -*- coding:utf-8 -*-

from Tkinter import *
import Pmw
import random
word_list = [['钢笔', '铅笔'], ['月亮', '太阳'], ['美人痣', '青春痘'],
             ['陈奕迅', '张学友'], ['鸭脖', '鸡爪'], ['风衣', '毛衣']]
import time
import copy

class Game():

    def __init__(self, root, e, b, b2, b3, b4, w, dropdown):
        self.root = root
        self.man = 0
        self.undercover = 0
        self.civilian = 0
        self.entry = e
        self.n = 0
        self.b = b
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
        self.rerun_flg = False
        self.delete_flg = False
        self.key_word = self.get_word()
        self.first_flg = True
        self.n2 = 1
        self.dropdown = dropdown
        self.result = {}
        self.word_flg = False
        self.key_list = None
        self.vote_times = 1
        self.first_vote = True
        self.left_people = []
        self.undercover_code = 0
        self.w=w
        self.b['state'] = 'active'
        self.b2['state'] = 'disabled'
        self.b3['state'] = 'disabled'
        self.b.bind('<Button-1>', None)
        self.b2.bind('<Button-1>', None)
        self.b3.bind('<Button-1>', None)
        self.b2['text'] = '查看词语'
        self.w['text'] = ''
        self.w['fg'] = 'black'
    def game_start(self):
        if not self.rerun_flg:
            self.rerun_flg = True
            print 'inner if'
            print self.b, self.b2, self.b3
            self.b.bind('<Button-1>', self.check)
            self.b2['state']='disabled'
            if self.word_flg == True:
                self.b2['state'] = 'disabled'
            self.b3['state'] = 'disabled'
            print self.b,self.b2,self.b3
            self.b4.bind('<Button-1>', self.rerun)
    def check(self, event):
        n = self.entry.get()
        if not n.isdigit():
            self.w['text'] = '请输入(4-10)的正整数'
            self.w['fg'] = 'red'
        elif int(n)<4 or int(n)>10:
            self.w['text'] = '请输入(4-10)的正整数'
            self.w['fg'] = 'red'
            #'请输入(4-10)的正整数'
        else:
            n = int(n)
            self.man = n
            for i in range(1, self.man + 1):
                self.result[i] = 0
                self.left_people.append(i)
            self.w['text'] = '游戏开始，请第一个人查看词语'
            self.b['state'] = 'disabled'
            self.b2['state'] = 'active'
            self.b2.bind('<Button-1>', self.get_keyword_list)
    def get_word(self):
        i = random.randint(0, 5)
        word = word_list[i]
        return word

    def get_keyword_list(self, event):
        if self.first_flg:
            i2 = random.randint(0, 1)
            key_list = []
            for num in range(self.man):
                key_list.append(self.key_word[i2])
            i = random.randint(0, self.man-1)
            print 'i-%s'%i

            i_list = [0, 1]
            i_list.pop(i2)
            key_list[i] = self.key_word[i_list[0]]
            print 'self.key_word-%s'%self.key_word
            print 'i_list[0]-%s'%i_list[0]

            self.undercover_code = i + 1
            print 'self.undercover_code-%s'%self.undercover_code
            for i in key_list:
                print i

            self.key_list = key_list
        if self.n == self.man:
            self.word_flg = True
            self.w['text'] = '请玩家按顺序描述自己拿到的词语。描述完毕后开始投票'
            self.b3.bind('<Button-1>', self.click_vote)
            self.b3['state'] = 'active'

            self.b2.bind('<Button-1>', None)

            self.b2['state'] = 'disabled'
        else:
            print 'self.n-%s'%self.n
            self.b2.bind('<Button-1>', self.clean_word)
            self.w['text'] = '第%d个选手的身份是：%s， 看完请消除词语'%(self.n+1, self.key_list[self.n])
            self.b2['text'] = '消除词语'
            self.n += 1
            self.first_flg = False

    def clean_word(self, event):
        self.w['text'] = '请查\n看词\n语'
        self.b2['text'] = '查看词语'
        self.b2.bind('<Button-1>', self.get_keyword_list)
        if self.n == self.man:
            self.b2.bind('<Button-1>', None)

    def click_vote(self, event):
        code = copy.copy(self.left_people)
        print 'left_people-%s'%self.left_people
        if self.dropdown:
            self.dropdown.destroy()
        if self.n2 > len(self.left_people):
            eliminated_code = [x for x in self.result.keys() if self.result[x] == max(self.result.values())][0]
            print 'eliminated_code-%s'%eliminated_code
            print 'self.undercover_code-%s'%self.undercover_code
            if eliminated_code == self.undercover_code:
                self.w['text'] = '卧底已被找出，游戏结束。'
                self.w['fg'] = 'green'
                self.b3.bind('<Button-1>', None)
                self.game_over()
            elif len(self.left_people) <= 3:
                self.w['text'] = '卧底隐藏身份成功，平民失败。'
                self.w['fg'] = 'red'
                self.b3.bind('<Button-1>', None)
                self.game_over()
            else:
                self.w['text'] = '第%d轮投票结束，%d号选手被踢出，开始下一轮描述词语并投票'%(self.vote_times, eliminated_code)
                self.left_people.remove(eliminated_code)
                del self.result[eliminated_code]
                for key in self.result.keys():
                    self.result[key] = 0
                self.vote_times += 1
                self.n2 = 1
                self.man -= 1
        else:
            code.pop(self.n2 - 1)
            print code
            self.w['text'] = '请第%d号选手投票' % (self.left_people[self.n2-1])
            self.n2 += 1
        self.dropdown = Pmw.ComboBox(
                self.root,
                label_text = '',
                labelpos = 'nw',
                selectioncommand = self.vote,
                scrolledlist_items = code,
        )
        self.dropdown.grid(column=5,row=2)

    def vote(self, code):
        self.result[code] += 1
        print 'result-%s'%self.result
    def rerun(self, event):
        self.__init__(self.root, self.entry, self.b, self.b2, self.b3, self.b4,self.w, self.dropdown)
        if self.dropdown:
            print 'inner drif'

        self.w['text'] = '重新开始游戏，请输入人数并点击开始游戏。'
        self.game_start()
    def game_over(self):
        self.b3['state'] = 'disabled'
        self.b3.bind('<Button-1>', None)
#class Application(Frame):
#    def say_hi(self):
#        print "hi there, everyone!"
#
#    def createWidgets(self):
#        self.QUIT = Button(self)
#        self.QUIT["text"] = "QUIT"
#        self.QUIT["fg"]   = "red"
#        self.QUIT["command"] =  self.quit
#
#    #    self.QUIT.pack({"side": "left"})
#
#        self.hi_there = Button(self)
#        self.hi_there["text"] = "Hello",
#        self.hi_there["command"] = self.say_hi
#
#        self.hi_there.pack({"side": "left"})
#
#    def __init__(self, master=None):
#        Frame.__init__(self, master)
#        self.pack()
#        self.createWidgets()

if __name__ == '__main__':
    root = Tk()
    e = Entry(root)
    t = Text(root)


    t.insert(1.0, '游戏规则如下：\n游戏有卧底和平民 2 种身份。\n游戏根据在场人数大部分玩家拿到同一词语，其余玩家拿到与之相关的另一词语。\n' + \
             '每人每轮用一句话描述自己拿到的词语，既不能让卧底察觉，也要给同伴以暗示。\n每轮描述完毕，所有在场的人投票选出怀疑谁是卧底，得票最多的人出局。\n' + \
             '若卧底全部出局，则游戏结束。若卧底未全部出局，游戏继续。并反复此流程。\n' + \
             '若卧底撑到最后一轮（剩余总人数小于卧底初始人数的二倍时），则卧底获胜，反之，则平民胜利')
    t.grid(columnspan=7,row=0)
    w = Message(root, text='请输入游戏人数，开始游戏')
    w.grid(row=1, columnspan=7)
    b = Button(root, text='开始游戏', anchor=E)
    b2 = Button(root, text='查看词语', anchor=E)
    b3 = Button(root, text='投票', anchor=E)
    b4 = Button(root, text='重新开始', anchor=E)
    dropdown = Pmw.ComboBox(
        root,
        label_text='',
        labelpos='nw',
        selectioncommand=None,
        scrolledlist_items=[],
    )
    g = Game(root,e,b,b2,b3,b4,w,dropdown)
    g.game_start()
    b.grid(column=1,row=2)


    b2.grid(column=2,row=2)
    e.grid(column=0,row=2)
    b3.grid(column=3,row=2)
    b4.grid(column=4,row=2)
    dropdown.grid(column=5, row=2)

    root.mainloop()