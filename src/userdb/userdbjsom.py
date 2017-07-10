import json
import hashlib
import time

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
			"time" : <lastEditUNIXTime>,
			"snapshots" : [
				{
					"id" : <id>,
					"files" : [<fileName>, ...]
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
			"members" : []
			"time" : int(time.time()),
			"snapshots" : [
			{
				"id" : 0,
				"files" : []
			}] })
		return Group("""?""")
	
	def getGroups(self):
		
		
	def getGroup(self, grupId):
		pass
		
	def updateGruop(self, group):
		pass
		
	def removeGroup(self, groupId):
		pass
		
	# generators
	def genUser(self, user):
		return None
		
	def genGroup(self, group):
		return None
		
		
		
if __name__ == "__main__":
	db = UserDBJson("db.json")
	db.registerUser("Nikola", "car")
	db.registerUser("Stefan", "password")
	print (db.getUsers())
	print (db.dbDict)
	print (db.confirmUserLogin("Nikola", "password"))
	print (db.confirmUserLogin("Nikola", "car"))
	print (db.confirmUserLogin("Stefan", "Nikola"))
	print (db.confirmUserLogin("Stefan", "password"))
	
	
	
	