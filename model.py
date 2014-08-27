class Card():
	def __init__(self, front, back):
		self.front = front
		self.back = back
		self.known = False
		
	def getFront(self):
		return self.front

	def getBack(self):
		return self.back

	def setStatus(self, status):
		self.known = status

	def getStatus(self):
		return self.known

	def setFront(self, front):
		self.front = front

	def setBack(self, back):
		self.back = back
