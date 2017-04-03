#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import uno
import unohelper
from com.sun.star.lang import XServiceInfo
from com.sun.star.test import XSomethingA
IMPLE_NAME = "TestComponentA"
SERVICE_NAME = "com.sun.star.test.SomethingA"
class TestComponentA(unohelper.Base, XServiceInfo, XSomethingA):  
    # Java版ではcom.sun.star.uno.XWeakを継承しているがPythonでは必要かわからないので継承していない。
    def __init__(self, ctx, *args):
        self.ctx = ctx
        self.args = args
    # XSomethingA
    def methodOne(self,val):
        return val + " by Python UNO Component"
    # XServiceInfo
    def getImplementationName(self):
        return IMPLE_NAME
    def supportsService(self, name):
        return name == SERVICE_NAME
    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)
# Registration
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(TestComponentA, IMPLE_NAME, (SERVICE_NAME,),)
