#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
from create_rdb_from_idl import BASE_NAME
from create_manifest import createBK
import subprocess
import glob
import os
import shutil
import sys
from itertools import chain
def main():
    cwd = sys.path[0]  # このスクリプトのあるフォルダのパスを取得。
    oxt = os.path.join(cwd,BASE_NAME + ".oxt")  # 作成するoxtファイルの絶対パスを取得。
    createBK(oxt)  # すでにあるoxtファイルをbkに改名。
    os.chdir(os.path.join(cwd,"src"))  # 作業ディレクトリをsrcに変更。
    if not shutil.which("zip"):  # zipコマンドの有効を確認。
        print("The zip command must be valid for execution.")
        sys.exit()
    mani = glob.glob(os.path.join("META-INF","manifest.xml"))
    rdbs = glob.glob("*.rdb")
    comps = glob.glob("*.components") 
    pys = glob.glob("*.py")
    files = mani,rdbs,comps,pys
    if not all(files):
        names = "manifext.xml","*.rdb","*.components","*.py"
        for i,f in enumerate(files):  # 必須ファイルの存在確認。
            if not f:
                print(names[i] + "does not exist.")
                sys.exit()
    args = ["zip",oxt]
    args.extend(chain.from_iterable(files))
    subprocess.run(args)  # 必須ファイルをoxtファイルに収納。
    if os.path.exists("pythonpath"):  # pythonpathフォルダがあるとき
        exts = "py","mo"  # oxtファイルに含めるファイルの拡張子のタプル。
        files = []  # ファイルリストの初期化。
        for ext in exts:
            g = glob.glob(os.path.join("pythonpath","**","*." + ext),recursive=True)  # 指定拡張子のファイルのパスを取得。
            if g: files.extend(g)  # 指定拡張子のファイルがあるのならリストに追加。
        if not g:
            args = ["zip","-u",oxt]
            args.extend(files)
            subprocess.run(args)  # pythonpathフォルダをoxtファイルに収納。
if __name__ == "__main__":
    sys.exit(main())
    