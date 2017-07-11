
class Snapshot(object):
	
	def __init__(self, id=0):
		self.pages = [""] 
		self.index = 0
		self.id = id

	def addPage(self, code=""):
		self.pages.append(code)

	def getPages(self):
		return self.pages 

	def getId(self):
		return self.id 

	def setCurrentPage(self, index):
		self.index = index

	def getCurrentPage(self):
		return self.pages[self.index]

	def setCode(self, code):
		self.pages[self.index] = code

	def getCode(self):
		return self.pages[self.index]
