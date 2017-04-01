#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import sys
import os
cwd = sys.path[0]
program_path = os.path.dirname(sys.executable)  # programフォルダへのパスを取得。
regmerge = os.path.join(program_path,"regmerge")  # regmergeの取得。
sdk_path = os.path.join(os.path.dirname(program_path),"sdk")  # SDKフォルダへのパスを取得。
idlc = os.path.join(sdk_path,"bin","idlc")  # idlcの取得。
regview = os.path.join(program_path,"regview") 
idl = os.path.join(sdk_path,"idl")  # SDKのidlフォルダへのパスを取得。
myidl = os.path.join(cwd,"src","idl")  # PyDevプロジェクトのidlフォルダへのパスを取得。
import glob
myidls = glob.glob(os.path.join(myidl,"*.idl"))  # 自作idlファイルのリストを取得。
urds = glob.glob(os.path.join(myidl,"*.urd"))  # すでにあるurdファイルを取得。
for i in urds:  # すでにあるurdファイルを削除。
    os.remove(i)
import subprocess
for i in myidls:  # 各idlファイルをコンパイル。
    args = [idlc,"-I" + myidl,"-I" + idl, "-O" + myidl, i]
    subprocess.run(args)
project_name = os.path.basename(cwd)  # PyDevプロジェクト名を取得。    
urds = glob.glob(os.path.join(myidl,"*.urd"))  # urdファイルのリストを取得。
rdb = os.path.join(cwd,"src",project_name+".uno.rdb")  # uno.rdbファイルの絶対パスを取得。
args = [regmerge,rdb]
args.append("/UCR")  # mergeKeyName /URR(UNO core reflection)を追加。
args.extend(urds)  # urdファイル一覧を追加。
subprocess.run(args)  # urdファイルを一つのuno.rdbファイルにまとめる。
for i in urds:  # urdファイルを削除。
    os.remove(i)
args = [regview,rdb]
subprocess.run(args)  # rdbファイルの中身を出力。

