
import json

class User(object):

    def __init__(self, name, ip="", password=""):
        self.name = name 
        self.ip = ip 
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
        d = { "name": self.name, "ip": self.ip }
        return json.dumps(d)
