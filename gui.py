import controller
import os, sys 
from PyQt4 import QtGui, QtCore
from controller import FlashCardController

class NoTypeTextEdit(QtGui.QTextEdit):

	def keyPressEvent(self, event):
		event.ignore()

class OptionsTab(QtGui.QWidget):
	
	def __init__(self, parent, parentWidget):
		super(OptionsTab, self).__init__(parent)
		self.parent = parent
		self.parentWidget = parentWidget
		self.initUI()

		
	def initUI(self):
		pass
		self.layout = QtGui.QHBoxLayout() 

		self.apiKeysLayout = QtGui.QGridLayout()

		self.apiKeyTable = APIKeyTable(controller.apiKeys())
		self.apiKeysLayout.addWidget(self.apiKeyTable, 0, 1, 1, 2)

		editKeysButton = QtGui.QPushButton('Edit Keys', self)
		editKeysButton.clicked.connect(self.parentWidget.editKeys)
		self.apiKeysLayout.addWidget(editKeysButton, 1, 2, )
		self.layout.addLayout(self.apiKeysLayout)

		spacer = QtGui.QSpacerItem(200,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
		self.layout.addItem(spacer)

		verticalLine 	=  QtGui.QFrame()
		verticalLine.setFrameStyle(QtGui.QFrame.VLine)
		verticalLine.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
		self.layout.addWidget(verticalLine)

		self.rightSide = QtGui.QVBoxLayout()
		self.rightForm = QtGui.QFormLayout()
		self.delay = QtGui.QLineEdit(str(30))
		self.rightForm.addRow('Delay:', self.delay)

		self.rightSide.addLayout(self.rightForm)

		self.startButton = QtGui.QPushButton('Start', self)
		self.startButton.clicked.connect(self.startThread)
		self.rightSide.addWidget(self.startButton)

		self.layout.addLayout(self.rightSide)
		self.setLayout(self.layout)

	def getDelay(self):
		return int(self.delay.text())

	def startThread(self):
		self.parentWidget.start()
		self.startButton.setEnabled(False)

class FlashCardWindow(QtGui.QMainWindow):
	
	def __init__(self, cardFile = None):
		super(FlashCardWindow, self).__init__()
		self.deck = controller.makeCards(cardFile)
		self.controller = FlashCardController(self, self.deck)
		self.mainWidget = FlashCardWidget(self, self.controller)
		self.setCentralWidget(self.mainWidget)
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle('Macys Suit Getter')
		self.setGeometry(300,300,622,280)
		self.show()
	
	def showAbout(self):
		msgBox = QtGui.QMessageBox()
		msgBox.setWindowTitle("About")
		msgBox.setText("Copy a Macys Suit URl into the field and press the button. Enter a file name (with .csv or whatever). It makes it a csv.\nCreated by Luke Li on March 10, 2014")
		msgBox.exec_()

	def showResults(self):
		self.resultsScreen = ResultsWidget(self, self.controller) 
		self.setCentralWidget(self.resultsScreen)

	def showRestartDeck(self):
		newController = self.controller.newControllerUnknownCards()
		self.mainWidget = FlashCardWidget(self, newController)
		self.setCentralWidget(self.mainWidget)

	def showRestartAllDeck(self):
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
		card = QtGui.QLabel('Card')
		sideLabel = QtGui.QLabel('Front Side')
		mainLayout = QtGui.QVBoxLayout() 

		topBar = QtGui.QHBoxLayout()
		topBar.addWidget(self.cardLabel)
		topBar.addWidget(sideLabel)

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
			self.parent.showResults()

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

	def numCards(self):
		return self.controller.size()

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

		self.restartButton = QtGui.QPushButton('Restart', self)
		self.restartButton.clicked.connect(self.restart)
		self.restartAllButton = QtGui.QPushButton('Restart All', self)
		self.restartAllButton.clicked.connect(self.restartAll)
		self.endButton = QtGui.QPushButton('End', self)
		self.endButton.clicked.connect(self.next)

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


	def flip(self):
		if(self.showingFront):
			self.shownSide.setText(self.curCard.getBack())
			self.showingFront = False
		else:
			self.shownSide.setText(self.curCard.getFront())
			self.showingFront = True

	def next(self):
		if(controller.cardNumber + 1 < len(controller.deck)):
			controller.nextCard()
			self.showCard()
			self.updateGui()
		else:
			self.parent.showResults()

	def restart(self):
		self.parent.showRestartDeck()

	def restartAll(self):
		self.parent.showRestartAllDeck()

	def showCard(self):
		self.curCard = controller.getCurCard()
		self.showingFront = True

	def modifyKnown(self):
		cardStatus = controller.curCardKnown()
		controller.setCardStatus(not cardStatus)
		self.updateGui()


	def updateGui(self):
		self.shownSide.setText(self.curCard.getFront())
		self.cardLabel.setText("Card %s/%s" %(controller.cardNumber+1, len(controller.deck)))
		if(controller.cardNumber == 0):
			self.previousButton.setEnabled(False)
		else:
			self.previousButton.setEnabled(True)

		if(controller.cardNumber == len(controller.deck)-1):
			self.nextButton.setText("To Results!")
		else:
			self.nextButton.setText('Next')

		self.knownCheckbox.setChecked(controller.curCardKnown())

	def keyPressEvent(self, e):
		pass

class APIKeyTable(QtGui.QTableWidget):
	def __init__(self, data, *args):
		QtGui.QTableWidget.__init__(self, *args)
		self.data = data
		self.setColumnCount(2)
		headerLabels = ['API', 'Has Key']
		self.setHorizontalHeaderLabels(headerLabels)
		self.verticalHeader().hide()
		self.setData()
		self.resizeColumnsToContents()

	def setData(self):
		pass
		'''
		self.setRowCount(len(self.data))
		n = 0
		for key in self.data:
			labelItem = QtGui.QTableWidgetItem(key)
			labelItem.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
			hasKey = self.data[key] != ''
			valueItem =  QtGui.QTableWidgetItem(str(hasKey))
			valueItem.setFlags(QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled)
			self.setItem(n, 0, labelItem)
			self.setItem(n, 1, valueItem)
			n += 1
		'''

def main(cards):
	
	app = QtGui.QApplication(sys.argv)
	ex = FlashCardWindow(cards)
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()  