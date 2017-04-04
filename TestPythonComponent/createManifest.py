#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
from createRDB import BASE_NAME  # create_rdb_from_idl.pyからuno.rdb、.componentsファイル名を取得。

# tuples of a list of Python UNO Component Files: (file name,service implementation name, service name)
LST = [
    ("TestComponentA.py",'TestComponentA','com.sun.star.test.SomethingA'),
    ("TestComponentB.py",'TestComponentB','com.sun.star.test.SomethingB')  
       ]  # (Python UNO Componentファイル名、実装サービス名、サービス名)のタプルのリスト。


def createBK(path):  # pathのファイルがあれば拡張子bkを付ける。
    if os.path.exists(path):  # manifest.xmlファイルが存在するとき。
        bk = path + ".bk"  # バックアップファイル名の取得。
        if os.path.exists(bk): os.remove(bk)  # Windowsの場合は上書きできないので削除が必要。
        os.rename(path, bk)  # 既存のファイルを拡張子bkでバックアップ。   
def createComponentNode(args):
    py,IMP_NAME,SEV_NAME = args
    component = ET.Element("component",{'loader': 'com.sun.star.loader.Python',"uri":py})
    implementation = ET.SubElement(component,"implementation",{'name': IMP_NAME})
    service = ET.SubElement(implementation,"service",{'name': SEV_NAME})
    return component
def createFileEntry(root,ns,mt,fp):
    return ET.SubElement(root,"{" + ns + "}file-entry",{"{" + ns + "}media-type": mt,"{" + ns + "}full-path" :fp})
def createComponetsFile(cwd,component_file):  # .componentファイルの作成。
    comp = os.path.join(cwd,"src",component_file)  # PythonComponent.componentsのパスを取得。
    createBK(comp)
    with open(comp,"w",encoding="utf-8") as f:
        ns = "http://openoffice.org/2010/uno-components"
        root = ET.Element("{" + ns + "}components")
        for t in LST:
            root.append(createComponentNode(t))
        ET.register_namespace('', ns)
        tree = ET.ElementTree(root)
        tree.write(f.name,"utf-8",True)   
def createManifextFile(cwd,component_file,unordb_file):  # manifext.xmlファイルの作成
    meta = os.path.join(cwd,"src","META-INF")  # META-INFフォルダのパスを取得。
    mani = os.path.join(meta,"manifest.xml")  # manifest.xmlのパスを取得。
    if not os.path.exists(meta):  # META-INFフォルダがなければ作成する。
        os.mkdir(meta)
    createBK(mani)
    with open(mani,"w",encoding="utf-8") as f:
        ns = "http://openoffice.org/2001/manifest"
        root = ET.Element("{" + ns + "}manifest")
        createFileEntry(root,ns,"application/vnd.sun.star.uno-typelibrary;type=RDB", unordb_file)
        createFileEntry(root,ns,"application/vnd.sun.star.uno-components", component_file)
        tree = ET.ElementTree(root)
        ET.TreeBuilder(tree)
        ET.register_namespace('manifest', ns)
        tree.write(f.name,"utf-8",True)        
def main():
    component_file = BASE_NAME + ".components"
    unordb_file = BASE_NAME + ".uno.rdb"
    cwd = sys.path[0]  # このスクリプトのあるフォルダのパスを取得。
    createComponetsFile(cwd,component_file)  # .componentファイルの作成。
    createManifextFile(cwd,component_file,unordb_file)  # manifext.xmlファイルの作成
if __name__ == "__main__":
    sys.exit(main())    