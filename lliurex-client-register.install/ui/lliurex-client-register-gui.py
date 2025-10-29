#!/usr/bin/python3

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QUrl
from PySide2.QtGui import QIcon
from PySide2.QtQml import QQmlApplicationEngine

import sys
import LliurexClientRegister

app = QApplication()
app.setWindowIcon(QIcon("/usr/share/icons/hicolor/scalable/apps/lliurex-client-register.svg"));
engine = QQmlApplicationEngine()
engine.clearComponentCache()
context=engine.rootContext()
clientRegisterBridge=LliurexClientRegister.LliurexClientRegister(sys.argv[1])
context.setContextProperty("clientRegisterBridge",clientRegisterBridge)

url = QUrl("/usr/share/lliurex-client-register/rsrc/lliurex-client-register.qml")

engine.load(url)
if not engine.rootObjects():
	sys.exit(-1)

engine.quit.connect(QApplication.quit)
ret=app.exec_()
del engine
del app
sys.exit(ret)

