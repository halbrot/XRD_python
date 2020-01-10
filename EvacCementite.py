# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:12:45 2020

@author: ntn080465
"""

import subprocess
import shutil

def topas(SampDisp, CrySizeFix, fixvalue=25):
    
    def edit_bat(fname, inp):
        """
        実行するINPファイル名を書き換える．
        //実行時に引数で渡した方がよいかも・・・
        そもそも毎回inpファイルを生成するのでこの関数は不要！
        """
        cnt=0
        with open(fname + ".bat", 'r') as f1:
            tmp_list = []
            for row in f1:
                if cnt == 10:
                    row = "set inpname=" + inp
                    tmp_list.append(row)
                else:
                    tmp_list.append(row)
                cnt += 1
                
        with open("topas_from_py.bat", 'w') as f2:
            for i in range(len(tmp_list)):
                f2.write(tmp_list[i])
            
    
    def edit_inp(fname, SamplDisp, fixvalue):
        """
        CrySizeLの固定値の値を変更する．
        fname : INPファイルのファイル名
        SD (boolean) : SampleDisplacementの精密化をするかどうか．これによりCrySizeLの固定値の行が変わる．
        fix value : CrySizeL の固定値
        """
        cnt=0
        with open(fname + ".inp", 'r') as f1:
            tmp_list =[]
            if SampDisp == True:
                target_row = 46
            else:
                target_row = 45
            for row in f1:
                if cnt == target_row:
                    row = row[:58] + str(fixvalue) + row[60:]
                    tmp_list.append(row)
                else:
                    tmp_list.append(row)
                cnt += 1
    
        with open("for_python.inp", 'w') as f2:
            for i in range(len(tmp_list)):
                f2.write(tmp_list[i])
            
    if CrySizeFix:
        if SampDisp:
            inp = "Cementite-2_CS_SD"
            SD = True
        else:
            inp = "Cementite-2_CS"
            SD = False
        edit_inp(inp, SD, fixvalue)

    else:
        if SampDisp:
            inp = "Cementite-2_SD"
        else:
            inp = "Cementite-2"
        shutil.copyfile(inp + ".inp", "for_python.inp")
    
    
    #コマンドの第1引数にinpファイル名を，第2引数にfixvalue値をわたす．
    cmd = 'topas_from_py.bat ' + inp
    if CrySizeFix:
        cmd = cmd + " " + str(fixvalue)
    
    #subprocess.run(cmd)
    return cmd
    


import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        master.geometry('300x200')
        master.title("TOPASバッチ処理")
        self.create_widgets()
        
    def create_widgets(self):
        self.var0 = tk.BooleanVar()
        self.var0 = tk.BooleanVar()
        self.var1 = tk.BooleanVar()
        self.msg =tk.StringVar()
        
        self.label0 = tk.Label(root, text="TOPASの設定をチェックして実行ボタンを押してください．")
        self.label0.place(x=20, y=20)
        
        self.chk0 = tk.Checkbutton(root, variable = self.var0, text='Sample Displacement を精密化する')
        self.chk0.place(x=50, y=50)

        self.chk1 = tk.Checkbutton(root, variable = self.var1, text='CrySizeL を固定する', command=self.switch)
        self.chk1.place(x=50, y=80)

        self.txt = tk.Entry(width=10)
        self.txt.place(x=180, y=80)
        self.txt.config(state="disabled")

        self.btn = tk.Button(root, text="実行", width=20, command=self.pushed)
        self.btn.place(x=70, y=120)

        self.label1 = tk.Label(root, text="", )
        self.label1.place(x=80, y=160)
    
    def pushed(self):
        self.label1["text"] = ""
        if self.var1.get()==True and self.txt.get()=="":
            self.label1["text"] = "CrySizeL の値を入力してください．"
        else:
            cmd = topas(self.var0.get(), self.var1.get(), self.txt.get())
            subprocess.run(cmd)
            self.label1["text"] = "実行完了"

    def switch(self):
        if self.var1.get():
            self.txt.config(state="normal")
        else:
            self.txt.config(state="disabled")

root = tk.Tk()
app = Application(master=root)

     

app.mainloop()