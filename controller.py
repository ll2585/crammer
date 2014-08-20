import model

deck = None
cardNumber = 0

def getCurCard():
	return deck[cardNumber]

def makeCards(cards = None):
	global deck
	if(cards == None):
		deck = [model.Card("front1", "back1"), model.Card("front2", "back2")]
	else:
		loadCards(cards)

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

def loadCards(file):
	global deck
	import csv
	deck = []
	with open(file) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			c = model.Card(row[0], row[1])
			deck.append(c)

def size():
	return len(deck)