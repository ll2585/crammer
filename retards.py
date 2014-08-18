import controller
import os, sys 
from PyQt4 import QtGui, QtCore


class MainWidget(QtGui.QWidget):
	
	def __init__(self, parent):
		super(MainWidget, self).__init__(parent)
		self.parent = parent
		#controller.makeCards("tem")
		#self.initUI()
		
	def initUI(self):

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

		mainLayout.addLayout(topBar)
		mainLayout.addLayout(middleBar)
		self.setLayout(mainLayout)

	def keyPressEvent(self, e):
		print(e.key())
		if (e.key() == QtCore.Qt.Key_Right):
			self.close()

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



class MainWindow(QtGui.QMainWindow):
	
	def __init__(self):
		super(MainWindow, self).__init__()
		self.mainWidget = MainWidget(self) 
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

def main():
	
	app = QtGui.QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()  