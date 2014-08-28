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
	def __init__(self, cards = None):
		self.cards = self.loadCards(cards) if(cards) else []

	def addCard(self, card):
		self.cards.append(card)

	def size(self):
		return len(self.cards)

	def loadCards(self, file):
		import csv
		cards = []
		with open(file, encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				c = Card(row[0], row[1])
				cards.append(c)
		return cards

	def getCardAt(self, location):
		return self.cards[location]

	def knownCards(self):
		result = 0
		for c in self.cards:
			result += c.getStatus()
		return result

	def unknownDeck(self):
		unknownDeck = Deck()
		for c in self.cards:
			if(not c.getStatus()):
				unknownDeck.addCard(c)
		return unknownDeck