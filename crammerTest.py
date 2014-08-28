import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
import gui
import model

class GuiTester(unittest.TestCase):
	def setUp(self):
		'''Create the GUI'''
		self.app = QApplication(sys.argv)


	def test_demo(self):
		self.form = gui.MainWindow("test.csv")
		self.assertEqual(self.form.mainWidget.numCards(), 8)

	def test_knowZero(self):
		self.form = gui.MainWindow("test.csv")
		nextButton = self.form.mainWidget.nextButton
		self.assertEqual(self.form.mainWidget.numCards(), 8)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		self.assertEqual(self.form.mainWidget.knownCards(), 0)

	def test_knowThree(self):
		self.form = gui.MainWindow("test.csv")
		nextButton = self.form.mainWidget.nextButton
		knownCheckbox = self.form.mainWidget.knownCheckbox
		self.assertEqual(self.form.mainWidget.numCards(), 8)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownCheckbox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownCheckbox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownCheckbox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		results = self.form.resultsScreen
		self.assertEqual(self.form.mainWidget.knownCards(), 3)
		self.assertTrue('3/8' in results.knownLabel.text())
		restartAllButton = results.restartAllButton
		QTest.mouseClick(restartAllButton, Qt.LeftButton)
		cardScreen = self.form.mainWidget
		self.assertEqual(self.form.mainWidget.numCards(), 8)


	def test_restartThree(self):
		
		self.form = gui.MainWindow("test.csv")
		nextButton = self.form.mainWidget.nextButton
		knownCheckbox = self.form.mainWidget.knownCheckbox
		self.assertEqual(self.form.mainWidget.numCards(), 8)
		self.assertFalse(self.form.mainWidget.knownCheckbox.isChecked())
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownCheckbox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		self.assertFalse(self.form.mainWidget.knownCheckbox.isChecked())
		knownCheckbox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		knownCheckbox.click()
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		results = self.form.resultsScreen
		self.assertEqual(self.form.mainWidget.knownCards(), 3)
		self.assertTrue('3/8' in results.knownLabel.text())
		restartButton = results.restartButton
		QTest.mouseClick(restartButton, Qt.LeftButton)
		cardScreen = self.form.mainWidget
		self.assertEqual(self.form.mainWidget.numCards(), 5)

	def tearDown(self):
		self.form = None

class ModelTester(unittest.TestCase):
	def test_emptydeck(self):
		deck = model.Deck()
		self.assertEqual(deck.size(), 0)

	def test_loaddeck(self):
		deck = model.Deck("test.csv")
		self.assertEqual(deck.size(), 8)

if __name__ == "__main__":
	unittest.main()