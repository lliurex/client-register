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

	#def setServer

	def loadConfig(self):

		try:
			self.currentClientCart=self.client.ClientRegisterManager.get_current_cart()['return']
			print(self.currentClientCart)
			cmd="nfctl get NF_DEF_IP_NUMBER"
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			pout=p.communicate()[0].decode().strip()
			self.maxNumCart=int(pout)
			return True

		except Exception as e:
			print(str(e))
			return False

	#def loadConfig

	def applyChanges(self,cart):

		try:
			ret=self.client.ClientRegisterManager.set_cart(cart)
			result=[True,N4dManager.APPLY_CHANGES_SUCCESSFUL]
		except:
			result=[False,N4dManager.CHANGE_REGISTRATION_ERROR]
 
		self.loadConfig()
		return result

	#def applyChanges
		
#class N4dManager
