
from .snapshot import * 

class Group(object):
	
	def __init__(self, name, id, owner, members, snapshots):
		self.id = id 
		self.name = name 
		self.owner = owner				# owner object
		self.members = members			# member names
		self.snapshots = snapshots
		print (snapshots)
		
		self.currentSs = self.snapshots[-1]
		self.queue = []
		self.editing = None
		
		self.code = None
	
	def getName(self):
		return self.name

	def getId(self):
		return self.id
		
	def getOwner(self):
		return self.owner
	
	def addMember(self, name):
		self.members.append(name)
	
	def getMembers(self):
		return self.members 

	def setMembers(self, m):
		self.members = m

	def addSnapshot(self, s):
		self.snapshots.append(s)

	def getSnapshots(self):
		return self.snapshots

	def setSnapshots(self, s):
		self.snapshots = s 
		
	def hasSnapshot(self, snapshot):
		for ss in self.snapshots:
			if ss.getId() == snapshot.getId():
				return True
		return False
	
	def getCode(self):
		return self.code

	def setCode(self, code):
		self.code = code
	
	def whoEdits(self):
		return self.editing
	
	def setEditor(self, user):
		if self.editing != None and self.editing == user:
			return True
		if len(self.queue) == 0:
			if self.editing == None:
				self.editing = user
				return True
			else:
				self.queue.append(user)
		else:
			if self.editing == None:
				self.editing = self.queue[0]
				self.queue = self.queue[1:]
				return self.editing == user
			else:
				for q in self.queue:
					if q == user:
						return False
				self.queue.append(user)
				return False
		return False
	
	def releaseEditor(self, user):
		if self.editing == None: return
		print (user)
		name = user.getName()
		for i in range(len(self.queue)):
			if self.queue[i].getName() == name:
				del self.queue[i]
		if self.editing.getName() == name:
			self.editing = None
			if len(self.queue) > 0:
				self.editing = self.queue[0]
				del self.queue[0]

	def getCurrentSnapshot(self):
		return self.currentSs
	
