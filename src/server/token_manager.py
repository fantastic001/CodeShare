import time
import hashlib

class TokenManager:

	MAX_GUESTS = 1000

	def __init__(self):
		self.users = {}
		self.guests = {}
		self.tokens = {}
		self.guestsCo = 0
		self.nextGuestId = 1
		
	def newUser(self, user):
		if self.containsUser(user): return ""
		self.users[user] = { "token" : "u" + 
			hashlib.sha256((user.getName() + str(time.time())).encode("utf-8")).hexdigest(),
			"time" : time.time() }
		self.tokens[self.users[user]["token"]] = user
		return self.users[user]["token"]
	
	def newGuest(self):
		if self.guests == self.MAX_GUESTS: return "-1"
		guestname = "Guest" + str(self.nextGuestId)
		self.nextGuestId += 1
		self.guests[guestname] = { "token" : "g" + 
			hashlib.sha256((guestname + str(time.time())).encode("utf-8")).hexdigest(), 
			"time" : time.time() }
		self.tokens[self.guests[guestname]["token"]] = guestname
		self.guestsCo += 1
		return self.guests[guestname]["token"]
	
	def updateTokenTime(self, token):
		if not self.containsToken(token): return False
		self.tokens[token]["time"] = time.time()
		return True
		
	def getSessionTypeFromToken(self, token):
		return "user" if token[0] == "u" else "guest"
		
	def containsUser(self, user):
		if user == None: return False
		if len(user.getName()) == 0: return False
		return (user in self.users)
		
	def containsToken(self, token):
		return (token in self.tokens)
		
	def getToken(self, user):
		if self.containsUser(user): return self.users[user]
		return ""
		
	def getUser(self, token):
		if self.containsToken(token): return self.tokens[token]
		return ""
		
	def removeByUser(self, user):
		if not self.containsUsername(user): return False
		del self.tokens[self.users[user]]
		del self.users[user]
		return True
		
	def removeByToken(self, token):
		if not self.containsToken(token): return False
		if self.getSessionTypeFromToken(token) == "user":
			del self.users[self.tokens[token]]
		else:
			del self.guests[self.tokens[token]]
			self.guestsCo -= 1
		del self.tokens[token]
		return True

