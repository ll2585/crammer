import model

class Controller():
	def __init__(self, gui, hideKnownCards = False):
		self.gui = gui
		self.deck = None
		self.cardNumber = 0
		self.hideKnownCards = hideKnownCards

	def getCurCard(self):
		return self.getDeck().getCardAt(self.cardNumber)

	def makeCards(self, cards = None):
		self.deck = model.Deck(cards)

	def getDeck(self):
		if(self.hideKnownCards):
			return self.unknownDeck()
		else:
			return self.deck

	def nextCard(self):
		self.cardNumber += 1

	def previousCard(self):
		self.cardNumber -= 1

	def curCardKnown(self):
		return self.getCurCard().getStatus()

	def setCardStatus(self, status):
		self.getCurCard().setStatus(status)

	def size(self):
		return self.getDeck().size()

	def knownCards(self):
		return self.getDeck().knownCards()

	def reset(self):
		self.cardNumber = 0

	def unknownDeck(self):
		return self.deck.unknownDeck()
