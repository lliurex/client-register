#!/usr/bin/python3

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine

import sys
import LliurexClientRegister

app = QApplication()
app.setDesktopFileName("lliurex-client-register")
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
ret=app.exec()
del engine
del app
sys.exit(ret)

