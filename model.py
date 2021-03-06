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

class Deck():
	def __init__(self, f = None, cards = None):
		self.cards = [] if cards is None else cards
		if(f is not None):
			self.makeCards(f)

	def makeCards(self, f):
		import csv
		with open(f) as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				c = Card(row[0], row[1])
				self.cards.append(c)

	def shuffledCards(self):
		import copy, random
		copiedCards = copy.deepcopy(self)
		random.shuffle(copiedCards.cards)
		return copiedCards

	def size(self):
		return len(self.cards)

	def getCardAt(self, location):
		return self.cards[location]

	def knownCards(self):
		return sum(1 for x in self.cards if x.known)

	def getCards(self):
		return self.cards

	def restartAll(self):
		for c in self.cards:
			c.setStatus(False)