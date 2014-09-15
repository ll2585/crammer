from model import Deck

#non-specific methods
def makeCards(cards = None):
	return Deck(cards)

#for specific methods
class FlashCardController():
	def __init__(self, view, model):
		self.gui = view
		self.deck = model
		import copy
		self.originalDeck = copy.deepcopy(model)
		self.curCardCount = 0

	def getCurCard(self):
		return self.deck.getCardAt(self.curCardCount)

	def getCardNumber(self):
		return self.curCardCount

	def size(self):
		return self.deck.size()

	def curCardStatus(self):
		return self.getCurCard().getStatus()

	def setCardStatus(self, status):
		self.getCurCard().setStatus(status)

	def nextCard(self):
		self.curCardCount  += 1

	def previousCard(self):
		self.curCardCount  -= 1

	def knownCards(self):
		return self.deck.knownCards()

	def newControllerUnknownCards(self):
		unknownCards = [x for x in self.deck.getCards() if not x.known]
		unknownDeck = Deck(cards = unknownCards)
		return FlashCardController(self.gui, unknownDeck)
