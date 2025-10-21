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
				
	#def init

	def get_current_cart(self):

		current_cart=self.core.get_variable("CONTROLLED_CLASSROOM")

		return n4d.responses.build_successful_call_response(current_cart)

	#def get_current_cart

	def set_cart(self,new_cart):

		ret=self.core.set_variable("CONTROLLED_CLASSROOM",new_cart)

		cmd="natfree-tie update"
		os.system(cmd)

		return n4d.responses.build_successful_call_response()

	#def set_cart
		
#class ClientRegisterManager
