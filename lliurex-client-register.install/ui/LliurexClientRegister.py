#!/usr/bin/python3

from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os
import threading
import signal
import copy
import time
import N4dManager

signal.signal(signal.SIGINT, signal.SIG_DFL)

class GatherInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
	
	#def __init__
		
	def run(self,*args):
		
		time.sleep(1)
		self.ret=LliurexClientRegister.n4dMan.loadConfig()

	#def run

#class GatherInfo

class UpdateInfo(QThread):

	def __init__(self,*args):

		QThread.__init__(self)

		self.updateInfo=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):
		
		time.sleep(1)
		self.ret=LliurexClientRegister.n4dMan.applyChanges(self.updateInfo)
	
	#def run

#class UpdateInfo

class LliurexClientRegister(QObject):

	n4dMan=N4dManager.N4dManager()

	def __init__(self,ticket=None):

		QObject.__init__(self)
		self.initBridge(ticket)

	#def __init__

	def initBridge(self,ticket):

		self._settingsClientChanged=False
		self._showSettingsMessage=[False,"","Success"]
		self._showChangesDialog=False
		self._closeGui=False
		self._closePopUp=True
		self._currentStack=0
		self._currentOptionsStack=0
		self._currentClientCart=LliurexClientRegister.n4dMan.currentClientCart
		self._maxNumCart=LliurexClientRegister.n4dMan.maxNumCart
		self._showSpinner=True
		self.changeInRegistration=False
		LliurexClientRegister.n4dMan.setServer(ticket)
		self.gatherInfo=GatherInfo()
		self.gatherInfo.start()
		self.gatherInfo.finished.connect(self._loadConfig)

	#def initBridge

	def _loadConfig(self):		

		showError=False

		if self.gatherInfo.ret:
			self.currentClientCart=copy.deepcopy(LliurexClientRegister.n4dMan.currentClientCart)
			self.maxNumCart=LliurexClientRegister.n4dMan.maxNumCart
			if self.maxNumCart>0:
				self.currentStack=1
			else:
				showError=True
		else:
			shoWError=True

		if showError:
			if self.currentStack==0:
				self.showSpinner=False
			else:
				self.showSettingsMessage=[True,LliurexClientRegister.n4dMan.ERROR_LOADING_CONFIGURATION,"Error"]

	#def _loadConfig

	def _getCurrentStack(self):

		return self._currentStack

	#def _getCurrentStack

	def _setCurrentStack(self,currentStack):

		if self._currentStack!=currentStack:
			self._currentStack=currentStack
			self.on_currentStack.emit()

	#def _setCurrentStack

	def _getCurrentOptionsStack(self):

		return self._currentOptionsStack

	#def _getCurrentOptionsStack

	def _setCurrentOptionsStack(self,currentOptionsStack):

		if self._currentOptionsStack!=currentOptionsStack:
			self._currentOptionsStack=currentOptionsStack
			self.on_currentOptionsStack.emit()

	#def _setCurrentOptionsStack

	def _getShowSpinner(self):

		return self._showSpinner

	#def _getShowSpinner

	def _setShowSpinner(self,showSpinner):

		if self._showSpinner!=showSpinner:
			self._showSpinner=showSpinner
			self.on_showSpinner.emit()

	#def _setShowSpinner

	def _getCurrentClientCart(self):

		return self._currentClientCart

	#def _getCurrentClientCart

	def _setCurrentClientCart(self,currentClientCart):

		if self._currentClientCart!=currentClientCart:
			self._currentClientCart=currentClientCart
			self.on_currentClientCart.emit()

	#def _setCurrentClientCart

	def _getMaxNumCart(self):

		return self._maxNumCart

	#def _getMaxNumCart

	def _setMaxNumCart(self,maxNumCart):

		if self._maxNumCart!=maxNumCart:
			self._maxNumCart=maxNumCart
			self.on_maxNumCart.emit()

	#def _setCurrentClientCart

	def _getShowSettingsMessage(self):

		return self._showSettingsMessage

	#def _getShowSettingsMessage

	def _setShowSettingsMessage(self,showSettingsMessage):

		if self._showSettingsMessage!=showSettingsMessage:
			self._showSettingsMessage=showSettingsMessage
			self.on_showSettingsMessage.emit()

	#def _setShowSettingsMessage

	def _getShowChangesDialog(self):

		return self._showChangesDialog

	#def _showChangesDialog

	def _setShowChangesDialog(self,showChangesDialog):

		if self._showChangesDialog!=showChangesDialog:
			self._showChangesDialog=showChangesDialog
			self.on_showChangesDialog.emit()

	#def _setShowChangesDialog

	def _getSettingsClientChanged(self):

		return self._settingsClientChanged

	#def _getSettingsClientChanged

	def _setSettingsClientChanged(self,settingsClientChanged):

		if self._settingsClientChanged!=settingsClientChanged:
			self._settingsClientChanged=settingsClientChanged
			self.on_settingsClientChanged.emit()

	#def _setSettingsClientChanged

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp	

	def _setClosePopUp(self,closePopUp):
		
		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp		
			self.on_closePopUp.emit()

	#def _setClosePopUp	

	def _getCloseGui(self):

		return self._closeGui

	#def _getCloseGui	

	def _setCloseGui(self,closeGui):
		
		if self._closeGui!=closeGui:
			self._closeGui=closeGui		
			self.on_closeGui.emit()

	#def _setCloseGui

	@Slot(int)
	def updateCart(self,value):

		self.showSettingsMessage=[False,"","Success"]

		if value!=self.currentClientCart:
			self.currentClientCart=int(value)
		
		if self.currentClientCart!=LliurexClientRegister.n4dMan.currentClientCart:
			self.settingsClientChanged=True
		else:
			self.settingsClientChanged=False

	#def manageRegisterOptions
	
	@Slot()
	def applyChanges(self):

		self.showSettingsMessage=[False,"","Success"]
		self.closePopUp=False
		self.showChangesDialog=False
		self.updateInfoT=UpdateInfo(self.currentClientCart+1)
		self.updateInfoT.start()
		self.updateInfoT.finished.connect(self._updateInfoRet)

	#def applyChanges	

	def _updateInfoRet(self):

		if self.updateInfoT.ret[0]:
			self._initForm()
			self.showSettingsMessage=[True,self.updateInfoT.ret[1],"Success"]
			self.closeGui=True
		else:
			self.showSettingsMessage=[True,self.updateInfoT.ret[1],"Error"]
			self.closePopUp=True
			self.closeGui=False

	#def _updateInfoRet

	@Slot()
	def cancelChanges(self):

		self.closePopUp=False
		self.showChangesDialog=False
		self.showSettingsMessage=[False,"","Success"]
		self._initForm()

	#def cancelChanges

	def _initForm(self):

		self._loadConfig()
		self.changeInRegistration=False
		self.settingsClientChanged=False
		self.closePopUp=True
		self.closeGui=True

	#def _initForm

	@Slot(str)
	def manageChangesDialog(self,action):
		
		if action=="Accept":
			self.applyChanges()
		elif action=="Discard":
			self.cancelChanges()
		elif action=="Cancel":
			self.closeGui=False
			self.showChangesDialog=False

	#def manageChangesDialog

	@Slot(int)
	def manageTransitions(self,stack):

		if self.currentOptionsStack!=stack:
			self.currentOptionsStack=stack

	#def manageTransitions
	
	@Slot()
	def openHelp(self):
		
		self.helpCmd='xdg-open https://wiki.edu.gva.es/lliurex/tiki-index.php?page=Configuración-de-los-equipos-del-aula-móvil'
		
		self.openHelpT=threading.Thread(target=self._openHelpRet)
		self.openHelpT.daemon=True
		self.openHelpT.start()

	#def openHelp

	def _openHelpRet(self):

		os.system(self.helpCmd)

	#def _openHelpRet

	@Slot()
	def closeApplication(self):

		self.closeGui=False
		if self.settingsClientChanged:
			self.showChangesDialog=True
		else:
			self.closeGui=True

	#def closeApplication
	
	on_currentStack=Signal()
	currentStack=Property(int,_getCurrentStack,_setCurrentStack, notify=on_currentStack)
	
	on_currentOptionsStack=Signal()
	currentOptionsStack=Property(int,_getCurrentOptionsStack,_setCurrentOptionsStack, notify=on_currentOptionsStack)

	on_showSpinner=Signal()
	showSpinner=Property(bool,_getShowSpinner,_setShowSpinner,notify=on_showSpinner)
	
	on_currentClientCart=Signal()
	currentClientCart=Property(int,_getCurrentClientCart,_setCurrentClientCart, notify=on_currentClientCart)

	on_maxNumCart=Signal()
	maxNumCart=Property(int,_getMaxNumCart,_setMaxNumCart,notify=on_maxNumCart)

	on_settingsClientChanged=Signal()
	settingsClientChanged=Property(bool,_getSettingsClientChanged,_setSettingsClientChanged, notify=on_settingsClientChanged)

	on_showSettingsMessage=Signal()
	showSettingsMessage=Property('QVariantList',_getShowSettingsMessage,_setShowSettingsMessage,notify=on_showSettingsMessage)

	on_showChangesDialog=Signal()
	showChangesDialog=Property(bool,_getShowChangesDialog,_setShowChangesDialog,notify=on_showChangesDialog)

	on_closePopUp=Signal()
	closePopUp=Property(bool,_getClosePopUp,_setClosePopUp, notify=on_closePopUp)

	on_closeGui=Signal()
	closeGui=Property(bool,_getCloseGui,_setCloseGui, notify=on_closeGui)


#class LliurexClientRegister

