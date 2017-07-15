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
		self.dbFileName = dbFileName
		self.dbDict = json.load(open(dbFileName))
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
			"password" : password })
		return self.genUser(self.users[-1])
		
	def updateUser(self, user):
		for elem in self.users:
			if elem["username"] == user.getName():
				elem["password"] = user.getPassword()
		
	def confirmUserLogin(self, username, password):
		user = self.getUser(username)
		if user == None: return False
		return (user if user.getPassword() == password else None)
		
	def removeUser(self, username):
		for user in self.users:
			if user["username"] == username:
				del self.users[username]
				return True
		return False
		
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
			"owner" : owner.getUsername(),
			"members" : [],
			"snapshots" : [
			{
				"id" : 0
			}] })
		# create folder structure and 0-th snapshot
		self.dumpBase()
		return self.genGroup(self.groups[-1])
	
	def getGroups(self):
		return [self.genGroup(group) for group in self.groups]
		
	def getGroup(self, groupId):
		for group in self.groups:
			if group["id"] == groupId:
				return self.genGroup(group)
		return None
		
	def updateGruop(self, group):
		for elem in self.groups:
			if elem["id"] == group.getId():
				elem["name"] = group.getName()
				elem["members"] = group.getMembers()
				# check for diferences in snapshot lists and delete or create files
				# use group.getCode
				elem["snapshots"] = [{ "id" : ss.getId() } for ss in group.getSnapshots()]
				return True
		return False
		
	def removeGroup(self, groupId):
		for group in self.groups:
			if group["id"] == groupId:
				del self.groups[groupId]
				# delete form disc
				return True
		return False
		
	def getCode(self, group, snapshot):
		for gr in self.groups:
			if gr["id"] == group.getId():
				ssId = snapshot.getId()
				try:
					with open("userdb/data/" + str(gr["id"]) + "/" + str(ssId)) as codeFile:
						return codeFile.read()
				except: 
					print ("Unable to open requested file: " + "userdb/data/" + str(gr["id"]) + "/" + str(ssId))
					return None
		return None
			
		
	# generators
	def genUser(self, user): # remove ip
		return User(user["username"], user["password"])
		
	def genGroup(self, group):
		return Group(group["name"], group["id"], self.getUser(group["owner"]), group["members"], 
			[Snapshot(ss["id"]) for ss in group["snapshots"]])
		
		
		
		
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
	
	
	
	
