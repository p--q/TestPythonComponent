#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import sys
import os
import glob
import subprocess

# This name will be rdb file name, .components file name, oxt file name.
BASE_NAME = "PythonComponent"  # これがrdbファイル名、.componentsファイル名、oxtファイル名になる。

def main():
    unordb_file = BASE_NAME + ".uno.rdb"
    # 各々のパスの取得。
    cwd = sys.path[0]  # このスクリプトのあるフォルダのパスを取得。
    program_path = os.path.dirname(sys.executable)  # programフォルダへのパスを取得。
    regmerge = os.path.join(program_path,"regmerge")  # regmergeの取得。
    sdk_path = os.path.join(os.path.dirname(program_path),"sdk")  # SDKフォルダへのパスを取得。
    idlc = os.path.join(sdk_path,"bin","idlc")  # idlcの取得。
    regview = os.path.join(program_path,"regview") 
    idl = os.path.join(sdk_path,"idl")  # SDKのidlフォルダへのパスを取得。
    myidl = os.path.join(cwd,"src","idl")  # PyDevプロジェクトのidlフォルダへのパスを取得。
    #myidlフォルダがなければmyidlフォルダを作成して終わる。
    if not os.path.exists(myidl):
        os.mkdir(myidl)
        print("Please create idl files in the idl folder.")
        sys.exit()
    #すべての存在確認をする。
    for p in [regmerge,idlc,regview,idl]:
        if not os.path.exists(p):
            print(os.path.basename(p) + " does not exit.")
            sys.exit()
    urds = os.path.join(myidl,"*.urd")  # urdファイルのパスを取得。
    for i in glob.iglob(urds):  # すでにあるurdファイルを削除。
        os.remove(i)
    for i in glob.iglob(os.path.join(myidl,"*.idl")):  # 各idlファイルをコンパイル。
        args = [idlc,"-I" + myidl,"-I" + idl, "-O" + myidl, i]
        subprocess.run(args)
    # urbファイルをrdbファイルへまとめる。  
    rdb = os.path.join(cwd,"src",unordb_file)  # uno.rdbファイルの絶対パスを取得。
    args = [regmerge,rdb]
    args.append("/UCR")  # mergeKeyName /UCR(UNO core reflection)を追加。
    args.extend(glob.glob(urds))  # urdファイル一覧を追加。
    subprocess.run(args)  # urdファイルを一つのuno.rdbファイルにまとめる。
    for i in glob.iglob(urds):  # 使用済みurdファイルを削除。
        os.remove(i)
    # rdbファイルの中身を確認。
    args = [regview,rdb]
    subprocess.run(args)  # rdbファイルの中身を出力。
if __name__ == "__main__":
    sys.exit(main())