
import json

class User(object):
	
	def __init__(self, name, password):
		self.name = name
		self.password = password
	
	def getName(self):
		return self.name 
	
	def getIp(self):
		return self.ip 
	
	def getPassword(self):
		return self.password
		
	def setPasswprd(self, password):
		self.password = password
	
	def to_json(self):
		d = { "name": self.name, "password": self.password }
		return json.dumps(d)
	