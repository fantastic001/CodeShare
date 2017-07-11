import json
import hashlib
import time

from server import *

"""from .user import *
from .snap_shot import *"""

"""
db = {
	"users" : [
		{
			"username" : <name>, 
			"password" : <pass>
		},...
	],
	"groups" : [
		{
			"id" : <id>,
			"name" : <name>,
			"owner" : <username>,
			"members" : [<username>,...]
			"snapshots" : [
				{
					"id" : <id>,
				},...
			]
		},...
	]
}
"""

class UserDBJson:
	
	def __init__(self, dbFileName):
		self.dbDict = { "users" : [], "groups" : [] }
		self.dbFileName = dbFileName
		with open(dbFileName) as dbFile:
			self.dbDict = json.load(dbFile)
		self.users = self.dbDict["users"]
		self.groups = self.dbDict["groups"]
		
	def dumpBase(self):
		with open(self.dbFileName, "w") as dbFile:
				dbFile.write(json.dumps(self.dbDict))
		
	def disconnect(self):
		self.dumpBase()
	
	# users 
	def registerUser(self, username, password):
		if self.getUser(username) != None: return None
		self.users.append({ 
			"username" : username, 
			"password" : hashlib.sha256(password.encode("utf-8")).hexdigest() })
		return self.genUser(self.users[-1])
		
	def updateUser(self, user):
		for elem in self.users:
			if elem["username"] == user.getName():
				elem["password"] = user.getPassword()
		
	def confirmUserLogin(self, username, password):
		user = self.getUser(username)
		if user == None: return False
		return True if user[password] == hashlib.sha256(password.encode("utf-8")).hexdigest() else False
		
	def getUsers(self):
		return [self.genUser(user) for user in self.users]
		
	def getUser(self, username):
		for user in self.users:
			if user["username"] == username:
				return self.genUser(user)
		return None
		
	# groups
	def registerGroup(self, owner, groupname = ""):
		newId = 0
		if len(self.groups) != 0:
			newId = self.groups[-1]["id"] + 1
		self.groups.append({
			"id" : newId,
			"name" : groupname,
			"owner" : owner.getUsermane(),
			"members" : [],
			"snapshots" : [
			{
				"id" : 0
			}] })
		return self.genGroup(self.groups[-1])
	
	def getGroups(self):
		return [self.genGroup(group) for group in self.groups]
		
	def getGroup(self, grupId):
		for group in self.groups:
			if group["id"] == groupId:
				return self.genGroup(group)
		return None
		
	def updateGruop(self, group):
		for elem in self.groups:
			if elem["id"] == group.getId():
				elem["name"] = group.getName()
				elem["members"] = group.getMembers()
				elem["snapshots"] = [{ "id" : ss.getId() } for ss in group.getSnapshots()]
				return True
		return False
		
	def removeGroup(self, groupId):
		for group in self.groups:
			if group["id"] == groupId:
				del group[groupId]
				return True
		return False
		
	# generators
	def genUser(self, user): #name id password
		return User(user["name"], "ip legacy", user["password"])
		
	def genGroup(self, group):
		group = Group(group["name"], group["id"], getUser(group["owner"]))
		group.setMembers(group["members"])
		group.setSnapshots([Snapshot(ss["id"])] for ss in group["snapshots"])
		
		
		
"""if __name__ == "__main__":
	db = UserDBJson("db.json")
	db.registerUser("Nikola", "car")
	db.registerUser("Stefan", "password")
	print (db.getUsers())
	print (db.dbDict)
	print (db.confirmUserLogin("Nikola", "password"))
	print (db.confirmUserLogin("Nikola", "car"))
	print (db.confirmUserLogin("Stefan", "Nikola"))
	print (db.confirmUserLogin("Stefan", "password"))"""
	
	
	
	
