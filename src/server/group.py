
from .snapshot import * 

class Group(object):
	
	def __init__(self, name, id, owner):
		self.id = id 
		self.name = name 
		self.owner = owner
		self.members = []
		self.snapshots = []
		self.currentSs = len(self.snapshots) - 1
		self.queue = []
		self.editing = None
	
	def addMember(self, user):
		self.members.append(user)
	
	def getMembers(self):
		return self.members 

	def setMembers(self, m):
		self.members = m 
	
	def whoEdits(self):
		"""
		Returns User object who is currently editing
	
		None if noone edits
		"""
		return self.editing
	
	def getMemberByName(self, name):
		for user in self.members:
			if user.getName() == name:
				return user 
		return None
	
	def setEditorByName(self, name):
		user = self.getMemberByName(name)
		if self.editing != None and self.editing.getName() == name:
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
				return self.editing.getName() == name
			else:
				for q in self.queue:
					if q.getName() == name:
						return False
				self.queue.append(user)
				return False
		return False
	
	def releaseEditor(self, name):
		for i in range(len(self.queue)):
			if self.queue[i].getName() == name:
				del self.queue[i]
		if self.editing.getName() == name:
			self.editing = None
			if len(self.queue) > 0:
				self.editing = self.queue[0]
				del self.queue[0]		
	def getId(self):
		return self.id 

	def addSnapshot(self, s):
		self.snapshots.append(s)

	def getSnapshots(self):
		return self.snapshots

	def getCurrentSnapshot(self):
		if len(self.snapshots) == 0:
			self.addSnapshot(Snapshot(0))
		return self.snapshots[-1]
		#return self.snapshots[self.currentSs]

	def setSnapshots(self, s):
		self.snapshots = s 
	
	def getName(self):
		return self.name 
	
	def getCode(self):
		return self.getCurrentSnapshot().getCode()

	def setCode(self, code):
		self.getCurrentSnapshot().setCode(code)
		
	def getOwner(self):
		return self.owner
	
