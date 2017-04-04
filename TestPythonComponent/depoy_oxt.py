#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import glob
cwd = sys.path[0]  # このスクリプトのあるフォルダのパスを取得。
oxt = glob.glob(os.path.join(cwd,"*.oxt"))  # 作成するoxtファイルの絶対パスのリストを取得。
if oxt:
    oxt_path = oxt[0]
    oxt_name = os.path.basename(oxt_path)
    uno_path = os.path.dirname(os.environ["UNO_PATH"])  # programフォルダへのパスを取得。
    unopkg = os.path.join(uno_path,"program","unopkg") 
    args = [unopkg,"remove",oxt_name]
    subprocess.run(args) 
    args = [unopkg,"add",oxt_path]
    subprocess.run(args) 
