import model

class Controller():
	def __init__(self, gui):
		self.gui = gui
		self.deck = None
		self.cardNumber = 0

	def getCurCard(self):
		return self.deck.getCardAt(self.cardNumber)

	def makeCards(self, cards = None):
		self.deck = model.Deck(cards)

	def nextCard(self):
		self.cardNumber += 1

	def previousCard(self):
		self.cardNumber -= 1

	def curCardKnown(self):
		return self.getCurCard.getStatus()

	def setCardStatus(self, status):
		self.getCurCard.setStatus(status)

	def size(self):
		return len(self.deck)

	def knownCards(self):
		self.known = 0
		for c in self.deck:
			if c.getStatus():
				self.known += 1
		return self.known
