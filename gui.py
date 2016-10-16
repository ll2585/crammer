import controller
import sys
from PyQt4 import QtGui, QtCore
from controller import FlashCardController


class FlashCardWindow(QtGui.QMainWindow):
	
	def __init__(self, cardFile = None):
		super(FlashCardWindow, self).__init__()
		self.deck = controller.makeCards(cardFile)
		self.controller = FlashCardController(self, self.deck)
		self.curController = self.controller
		self.mainWidget = FlashCardWidget(self, self.curController)
		self.setCentralWidget(self.mainWidget)
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle('Crammer')
		self.setGeometry(300,300,622,280)
		self.show()

	def showResults(self, controller):
		self.resultsScreen = ResultsWidget(self, controller) 
		self.setCentralWidget(self.resultsScreen)

	def showRestartDeck(self, controller):
		self.mainWidget = FlashCardWidget(self, controller)
		self.setCentralWidget(self.mainWidget)

	def showRestartAllDeck(self):
		self.controller.restartAll()
		self.mainWidget = FlashCardWidget(self, self.controller)
		self.setCentralWidget(self.mainWidget)

class FlashCardWidget(QtGui.QWidget):
	
	def __init__(self, parent, controller):
		super(FlashCardWidget, self).__init__(parent)
		self.parent = parent
		self.controller = controller
		self.initUI()
		
	def makeFocus(self):
		self.setFocus()
		self.grabKeyboard()

	def initUI(self):
		if not self.hasFocus():
			self.makeFocus()
		self.cardLabel = QtGui.QLabel()
		mainLayout = QtGui.QVBoxLayout() 

		topBar = QtGui.QHBoxLayout()
		topBar.addWidget(self.cardLabel)

		middleBar = QtGui.QHBoxLayout()
		self.shownSide = QtGui.QLabel()
		middleBar.addWidget(self.shownSide)

		self.previousButton = QtGui.QPushButton('Last', self)
		self.previousButton.clicked.connect(self.previous)
		flipButton = QtGui.QPushButton('Flip', self)
		flipButton.clicked.connect(self.flip)
		self.knownCheckbox = QtGui.QCheckBox('Known', self)
		self.knownCheckbox.clicked.connect(self.modifyKnown)
		self.nextButton = QtGui.QPushButton('Next', self)
		self.nextButton.clicked.connect(self.next)

		bottomBar = QtGui.QHBoxLayout()
		bottomBar.addWidget(self.previousButton)
		bottomBar.addWidget(flipButton)
		bottomBar.addWidget(self.knownCheckbox)
		bottomBar.addWidget(self.nextButton)

		mainLayout.addLayout(topBar)
		mainLayout.addLayout(middleBar)
		mainLayout.addLayout(bottomBar)
		self.setLayout(mainLayout)

		self.showCard()
		self.updateGui()

	def flip(self):
		if(self.showingFront):
			self.shownSide.setText(self.curCard.getBack())
			self.showingFront = False
		else:
			self.shownSide.setText(self.curCard.getFront())
			self.showingFront = True

	def next(self):
		if(self.controller.getCardNumber() + 1 < self.controller.size()):
			self.controller.nextCard()
			self.showCard()
			self.updateGui()
		else:
			self.releaseKeyboard()
			self.parent.showResults(self.controller)

	def previous(self):
		if(self.controller.getCardNumber() > 0):
			self.controller.previousCard()
			self.showCard()
			self.updateGui()
		else:
			print("OOPS")

	def showCard(self):
		self.curCard = self.controller.getCurCard()
		self.showingFront = True

	def modifyKnown(self):
		cardStatus = self.controller.curCardStatus()
		self.controller.setCardStatus(not cardStatus)
		self.updateGui()

	def updateGui(self):
		self.shownSide.setText(self.curCard.getFront())
		self.cardLabel.setText("Card %s/%s" %(self.controller.getCardNumber()+1, self.controller.size()))
		if(self.controller.getCardNumber() == 0):
			self.previousButton.setEnabled(False)
		else:
			self.previousButton.setEnabled(True)

		if(self.controller.getCardNumber() == self.controller.size()-1):
			self.nextButton.setText("To Results!")
		else:
			self.nextButton.setText('Next')

		self.knownCheckbox.setChecked(self.controller.curCardStatus())

	def keyPressEvent(self, e):
		if (e.key() == QtCore.Qt.Key_Right):
			self.next()
		elif(e.key() == QtCore.Qt.Key_Left):
			self.previous()
		elif(e.key() == QtCore.Qt.Key_Down or e.key() == QtCore.Qt.Key_Up):
			self.flip()
		elif(e.key() == QtCore.Qt.Key_Space):
			self.modifyKnown()


class ResultsWidget(QtGui.QWidget):
	
	def __init__(self, parent, controller):
		super(ResultsWidget, self).__init__(parent)
		self.parent = parent
		self.controller = controller
		self.initUI()
		
	def initUI(self):
		if not self.hasFocus():
			self.setFocus()
			self.grabKeyboard()
		self.knownCards = self.controller.knownCards()
		self.statusLabel = QtGui.QLabel("Try Harder!")
		self.knownLabel = QtGui.QLabel('You knew %s/%s cards!' %(self.controller.knownCards(), self.controller.size()))
		self.keepCheckBox = QtGui.QCheckBox('Keep all known cards', self)
		mainLayout = QtGui.QVBoxLayout() 

		self.restartButton = QtGui.QPushButton('Restart This Session', self)
		self.restartButton.clicked.connect(self.restart)
		self.restartAllButton = QtGui.QPushButton('Restart All the Cards', self)
		self.restartAllButton.clicked.connect(self.restartAll)
		self.endButton = QtGui.QPushButton('End', self)
		self.endButton.clicked.connect(self.end)

		restartBar = QtGui.QHBoxLayout()
		restartBar.addWidget(self.restartButton)
		restartBar.addWidget(self.restartAllButton)

		bottomBar = QtGui.QHBoxLayout()
		bottomBar.addWidget(self.endButton)

		mainLayout.addWidget(self.statusLabel)
		mainLayout.addWidget(self.knownLabel)
		mainLayout.addWidget(self.keepCheckBox)
		mainLayout.addLayout(restartBar)
		mainLayout.addLayout(bottomBar)
		self.setLayout(mainLayout)

	def end(self):
		import sys
		sys.exit()

	def restart(self):
		newController = self.controller if self.keepCheckBox.isChecked() else self.controller.newControllerUnknownCards()
		newController.restartAll()
		self.parent.showRestartDeck(newController)

	def restartAll(self):
		self.controller.init()
		self.parent.showRestartAllDeck()


def main(cards):

	app = QtGui.QApplication(sys.argv)
	ex = FlashCardWindow(cards)
	sys.exit(app.exec_())
