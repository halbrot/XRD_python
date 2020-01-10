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
    
    res = subprocess.run(cmd)
    
    


import tkinter as tk

root = tk.Tk()
root.geometry('300x200')
root.title("TOPASバッチ処理")

var0 = tk.BooleanVar()
var1 = tk.BooleanVar()
msg =tk.StringVar()


def pushed():
    label1["text"] = "実行中"
    if var1.get()==True and txt.get()=="":
        label1["text"] = "CrySizeL の値を入力してください．"
    else:
        topas(var0.get(), var1.get(), txt.get())
        label1["text"] = "実行完了"

def switch():
    if var1.get():
        txt.config(state="normal")
    else:
        txt.config(state="disabled")
        
label0 = tk.Label(root, text="TOPASの設定をチェックして実行ボタンを押してください．")
label0.place(x=20, y=20)


chk0 = tk.Checkbutton(root, variable = var0, text='Sample Displacement を精密化する')
chk0.place(x=50, y=50)

chk1 = tk.Checkbutton(root, variable = var1, text='CrySizeL を固定する', command=switch)
chk1.place(x=50, y=80)

txt = tk.Entry(width=10)
txt.place(x=180, y=80)
txt.config(state="disabled")

btn = tk.Button(root, text="実行", width=20, command=pushed)
btn.place(x=70, y=120)

label1 = tk.Label(root, text="", )
label1.place(x=80, y=160)

tk.mainloop()