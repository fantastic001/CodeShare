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
		
	def newUser(self, username):
		if self.containsUsername(username): return ""
		self.users[username] = { "token" : "u" + hashlib.sha256(username + str(time.time())).hexdigest(), "time" : time.time() }
		self.tokens[self.users[username]["token"]] = username
		return self.users[username]["token"]
	
	def newGuest(self):
		if self.guests == MAX_GUESTS: return "-1"
		guestname = "Guest" + str(self.nextGuestId)
		self.nextGuestId += 1
		self.guests[guestname] = { "token" : "g" + hashlib.sha256(guestname + str(time.time())).hexdigest(), "time" : time.time() }
		self.tokens[self.guests[guestname]["token"]] = guestname
		self.guestsCo += 1
		return self.guests[guestname]["token"]
	
	def updateTokenTime(self, token):
		if not self.containsToken(token): return False
		self.tokens[token]["time"] = time.time()
		return True
		
	def getSessionTypeFromToken(self, token):
		return "user" if token[0] == "u" else "guest"
		
	def containsUsername(self, username):
		if len(username) == 0 return False
		return (username in self.users)
		
	def containsToken(self, token):
		return (token in self.tokens)
		
	def getToken(self, username):
		if self.containsUsername(username): return self.users[username]
		return ""
		
	def getUser(self, token):
		if self.containsToken(token): return self.tokens[token]
		return ""
		
	def removeByUser(self, username):
		if not self.containsUsername(username) return False
		del self.tokens[self.users[username]]
		del self.users[username]
		return True
		
	def removeByToken(self, token):
		if not self.containsToken(token) return False
		if self.getSessionTypeFromToken(token) == "user":
			del self.users[self.tokens[token]]
		else:
			del self.guests[self.tokens[token]]
			self.guestsCo -= 1
		del self.tokens[token]
		return True

