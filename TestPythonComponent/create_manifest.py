#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
def createbk(path):
    if os.path.exists(path):  # manifest.xmlファイルが存在するとき。
        bk = path + ".bk"  # バックアップファイル名の取得。
        if os.path.exists(bk): os.remove(bk)  # Windowsの場合は上書きできないので削除が必要。
        os.rename(path, bk)  # 既存のファイルを拡張子bkでバックアップ。   
cwd = sys.path[0]  # このスクリプトのあるフォルダのパスを取得。
# .componentファイルの作成。
comp = os.path.join(cwd,"src","PythonComponent.components")  # PythonComponent.componentsのパスを取得。
createbk(comp)
with open(comp,"w",encoding="utf-8") as f:
    ns = "http://openoffice.org/2010/uno-components"
    root = ET.Element("{" + ns + "}components")
    root.append(ET.Element('component', attrib={'loader': 'com.sun.star.loader.Python',"uri":"TestComponentA.py"}))
    
    
    
    
    
    ET.register_namespace('', ns)
    # wrap it in an ElementTree instance, and save as XML
    tree = ET.ElementTree(root)
    tree.write(f.name,"utf-8",True)


# manifext.xmlファイルの作成
# meta = os.path.join(cwd,"src","META-INF")  # META-INFフォルダのパスを取得。
# mani = os.path.join(meta,"manifest.xml")  # manifest.xmlのパスを取得。
# if not os.path.exists(meta):  # META-INFフォルダがなければ作成する。
#     os.mkdir(meta)
# createbk(mani)

    
    