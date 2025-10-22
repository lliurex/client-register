#!/usr/bin/python3
import sys
import os
import threading
import subprocess
import copy
import time
import n4d.server.core as n4dcore
import n4d.responses
import xmlrpc.client as n4dclient
import ssl
import re

class ClientRegisterManager:
	
	def __init__(self):
		
		self.core=n4dcore.Core.get_core()
		self.current_cart=1
				
	#def init

	def get_current_cart(self):

		ret=self.core.get_variable("CONTROLLED_CLASSROOM")
		if ret["status"]==0:
			self.current_cart=ret["return"]
		return n4d.responses.build_successful_call_response(ret)

	#def get_current_cart

	def set_cart(self,new_cart):

		ret=self.core.set_variable("CONTROLLED_CLASSROOM",new_cart)

		if ret["status"]==0:
			cmd="natfree-tie update"
			p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			pout,perror=p.communicate()
			return_code=p.returncode
			if return_code==0:
				result=[True,ret]
			else:
				self.core.set_variable("CONTROLLED_CLASSROOM",self.current_cart)
				result=[False,perror.decode()]
		else:
			result=[False,ret]

		return n4d.responses.build_successful_call_response(result)

	#def set_cart
		
#class ClientRegisterManager
