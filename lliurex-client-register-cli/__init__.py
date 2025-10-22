#!/usr/bin/env python3

import os
import subprocess
import n4d.client
import sys
import syslog
import pwd
import grp
import getpass
import signal
import codecs

signal.signal(signal.SIGINT,signal.SIG_IGN)

class ClientRegisterCliManager(object):

	def __init__(self,mode):
		
		self.currentUser=""
		self.unattendedMode=mode
		self.currentCart=0
		self.n4dClient=n4d.client.Client()
		self._getCurrentUser()

	#def __init__

	def createClient(self):

		if self.currentUser!="":
			password=getpass.getpass('   [Client-Register]: Enter your password:')
			client=n4d.client.Client("https://localhost:9779",self.currentUser,password)
			
			try:
				ticket=client.get_ticket()
				self.n4dClient=n4d.client.Client(ticket=ticket)
			except Exception as e:
				msg="Authentication failed. Unable to execute action"
				self.writeLog(msg)
				print("   [Client-Register]: %s"%msg)
				sys.exit(1)
		else:
			masterKey=n4d.client.Key.master_key()
			
			if masterKey.valid():
				self.n4dClient=n4d.client.Client(key=masterKey)
			else:
				print('   [Client-Register]: You need root privilege to run this tool')

	#def createClient

	def showCurrentConfig(self):

		ret=self._getInfo("Initial")

		if ret==0:
			print('   [Client-Register]: Current cart assigned to laptop: %s'%self.currentCart)
			return 0
		else:
			print('   [Client-Register]: Error loading configuration')
			return 1

	#def showCurrentConfig

	def setCart(self,cart):

		ret=self._getInfo("Initial")
		self.writeLog("Changes in client register. Changed cart to: %s"%cart)

		if ret==0:
			maxNumCart=self._getMaxCart()

			if int(cart)<=maxNumCart:
				if int(cart)!=int(self.currentCart):
					if not self.unattendedMode:
						response=input('   [Client-Register]: Do you want to activate the automatic connection to the indicated Wifi? (yes/no)): ').lower()
					else:
						response='yes'

					if response.startswith('y'):
						self.createClient()
						try:
							ret=self.n4dClient.ClientRegisterManager.set_cart(cart)
							if ret[0]:
								msg="Changes in client-register. Result successfull"
								print('   [Client-Register]: %s'%msg)
								self.writeLog(msg)
								ret=self._getInfo('End')
								return 0
							else:
								print('   [Client-Register]: Unable to change the cart')
								self.writeLog("Changes in client-register. Error: %s"%ret[1])
								return 1
						except Exception as e:
							print('   [Client-Register]: Unable to change the cart')
							self.writeLog("Changes in client-register. Error: %s"%str(e))
							return 1
					else:
						print('   [Client-Register]: Action canceled')
						self.writeLog("Changes in client-register. Aborted")
						return 0
				else:
					print('   [Client-Register]: The indicated cart already assigned. Nothing to do')
					self.writeLog("Changes in client-register. Nothing to do")
					return 0
			else:
				print('   [Client-Register]: The cart to be assigned is not valid')
				self.writeLog("Changes Abort: Cart value is not valid: %s"%str(cart))
				return 1
		else:
			print('   [Client-Register]: Unable to get config')
			return 1

	#def setCart

	def _getInfo(self,step="Initial"):

		try:
			self.writeLog("Client-Register. %s configuration:"%step)
			ret=self.n4dClient.ClientRegisterManager.get_current_cart()
			if ret['status']==0:
				self.currentCart=ret["return"]
				self.writeLog("- Current cart assigned: %s"%self.currentCart)
				return 0
			else:
				self.writeLog("- Error loading configuration: %s"%str(ret))
				return 1
		except Exception as e:
			self.writeLog("- Error loading configuration: %s"%str(e))
			return 1

	#def _getInfo

	def _getMaxCart(self):

		cmd="nfctl get NF_DEF_IP_NUMBER"
		p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		pout=p.communicate()[0].decode().strip()
		
		return int(pout)

	#def _getMaxCart

	def _getCurrentUser(self):

		sudoUser=""
		loginUser=""
		pkexecUser=""

		try:
			sudoUser=(os.environ["SUDO_USER"])
		except:
			pass
		try:
			loginUser=os.getlogin()
		except:
			pass

		try:
			cmd="id -un $PKEXEC_UID"
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			pkexecUser=p.communicate()[0].decode().strip()
		except Exception as e:
			pass

		if pkexecUser!="root" and pkexecUser!="":
			self.currentUser=pkexecUser

		elif sudoUser!="root" and sudoUser!="":
			self.currentUser=sudoUser
			
		else:
			self.currentUser=loginUser

		self.writeLog("Init session in lliurex-Client-Register CLI")
		
		if loginUser!="":
			self.writeLog("User login in CLI: %s"%self.currentUser)
		else:
			self.writeLog("User login in CLI: No current user detected. A script may have been executed at login")

		if self.unattendedMode:
			self.currentUser=""

		self.writeLog("Unattended Mode:%s"%(str(self.unattendedMode)))

	#def _getCurrentUser

	def writeLog(self,msg):

		syslog.openlog("CLIENT-REGISTER")
		syslog.syslog(msg)

	#def writeLog

#class ClientRegisterCliManager	



