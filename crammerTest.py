import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
import gui

class GuiTester(unittest.TestCase):
	def setUp(self):
		'''Create the GUI'''
		self.app = QApplication(sys.argv)
		self.form = gui.MainWindow()

	def test_defaults(self):
		self.assertTrue('Card' in self.form.mainWidget.cardLabel.text())
		self.assertTrue('1' in self.form.mainWidget.cardLabel.text())

		#click next with mouse
		nextButton = self.form.mainWidget.nextButton
		QTest.mouseClick(nextButton, Qt.LeftButton)
		self.assertFalse('1' in self.form.mainWidget.cardLabel.text())

	def test_demo(self):
		self.form = gui.MainWindow("test.csv")
		self.assertEqual(self.form.mainWidget.numCards(), 8)

	def test_knowZero(self):
		nextButton = self.form.mainWidget.nextButton
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)
		QTest.mouseClick(nextButton, Qt.LeftButton)



if __name__ == "__main__":
	unittest.main()