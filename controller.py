import model

deck = None
cardNumber = 0

def getCurCard():
	return deck[cardNumber]

def makeCards(cards):
	global deck
	deck = [model.Card("front1", "back1"), model.Card("front2", "back2")]

def nextCard():
	global cardNumber
	cardNumber += 1

def previousCard():
	global cardNumber
	cardNumber -= 1

def curCardKnown():
	return deck[cardNumber].getStatus()

def setCardStatus(status):
	global deck
	deck[cardNumber].setStatus(status)