#!/usr/bin/python3

import n4d.client
import os
import subprocess
import sys
import syslog
import json
import codecs
import pwd
import grp

class N4dManager:

	APPLY_CHANGES_SUCCESSFUL=10
	CHANGE_REGISTRATION_ERROR=-10

	def __init__(self):

		self.debug=False
		self.currentClientCart=0
		self.maxNumCart=0
	
	#def __init__

	def setServer(self,ticket):
		
		ticket=ticket.replace('##U+0020##',' ')
		self.currentUser=ticket.split(' ')[2]
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)

		self.writeLog("Init session in lliurex-client-register GUI")
		self.writeLog("User login in GUI: %s"%self.currentUser)

	#def setServer

	def loadConfig(self,step="Initial"):

		try:
			self.writeLog("Client-Register. %s configuration:"%step)
			ret=self.client.ClientRegisterManager.get_current_cart()
			if ret['status']==0:
				self.currentClientCart=int(ret["return"])
				cmd="nfctl get NF_DEF_IP_NUMBER"
				p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
				pout=p.communicate()[0].decode().strip()
				self.maxNumCart=int(pout)
				self.writeLog("- Current cart assigned: %s"%self.currentClientCart)
				return True
			else:
				self.writeLog("- Error loading configuration: %s"%str(ret))
				return False

		except Exception as e:
			self.writeLog("- Error loading configuration: %s"%str(e))
			return False

	#def loadConfig

	def applyChanges(self,cart):

		try:
			self.writeLog("Changes in client-register. Changed cart to: %s"%cart)
			ret=self.client.ClientRegisterManager.set_cart(cart)
			if ret[0]:
				result=[True,N4dManager.APPLY_CHANGES_SUCCESSFUL]
				self.writeLog("Changes in client-register. Result successfull")
				self.loadConfig('End')
			else:
				self.writeLog("Changes in client-register. Error: %s"%ret[1])
				result=[False,N4dManager.CHANGE_REGISTRATION_ERROR]
		except Exception as e:
			self.writeLog("Changes in client-register. Error: %s"%str(e))
			result=[False,N4dManager.CHANGE_REGISTRATION_ERROR]
 
		return result

	#def applyChanges

	def writeLog(self,msg):

		syslog.openlog("CLIENT-REGISTER")
		syslog.syslog(msg)

	#def writeLog
		
#class N4dManager
