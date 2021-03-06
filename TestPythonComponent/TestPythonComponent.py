#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import officehelper
def connect():  # LibreOfficeをバックグラウンドで起動してコンポネントテクストを取得する。
    ctx = None
    try:
        ctx = officehelper.bootstrap()
        if ctx:
            print("Connected to a running office ...")
        return ctx
    except:
        pass
    return None
ctx = connect()
if ctx:
    smgr = ctx.getServiceManager()
    print("Using remote servicemanager")
    if not smgr:
        print( "ERROR: no service manager" )
SomethingB = smgr.createInstanceWithContext("TestComponentB", ctx)  # サービス名のcom.sun.star.test.SomethingBでもよい。
s = SomethingB.methodTwo("Hello World!")
print(s)
# soffice.binの終了処理。これをしないとLibreOfficeを起動できなくなる。
desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
from com.sun.star.beans import PropertyValue
prop = PropertyValue(Name="Hidden",Value=True)
desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, (prop,))  # バックグラウンドでWriterのドキュメントを開く。
terminated = desktop.terminate()  # LibreOfficeをデスクトップに展開していない時はエラーになる。
if terminated:
    print("The Office has been terminated.")  # 未保存のドキュメントがないとき。
else:
    print("The Office is still running. Someone else prevents termination.")  # 未保存のドキュメントがあってキャンセルボタンが押された時。
     