#!/usr/bin/env python
__author__ = "Jazmine"

#!/usr/bin/env python

import sys
from time import sleep
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication
from die import  *

class Demo(QMainWindow) :
    """Build a game demo."""
    die1 = die2 = None

    def __init__( self, parent=None ):
        super().__init__(parent)
        uic.loadUi("Demo.ui", self)
        self.die1 = Die(6)
        self.die2 = Die(6)
        self.firstRoll = True
        self.point = 0

        self.button.clicked.connect(self.buttonClickedHandler)

    def updateUI ( self ):
        self.resultsLabel.setText("Click!")        # Add your code here to update the GUI view so it matches the game state.

    def buttonClickedHandler( self ):
        totalRoll = self.die1.roll() + self.die2.roll()
        print('Roll =', totalRoll)
        if self.firstRoll == True:
            if totalRoll in [7, 11]:
                print("Shooter Wins, Pass Bets Win!")
            elif totalRoll in [2, 3, 12]:
                print("Shooter Loses, Don't Pass Bets Win!")
            else:
                self.point = totalRoll
                print('Point =', self.point)
                self.firstRoll = False
        else:
            if totalRoll == self.point:
                print("Shooter Wins, Pass Bets Win!")
            else:
                print("Shooter Loses, Don't Pass Bets Win!")
            self.firstRoll = True

        self.updateUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    diceApp = Demo()
    diceApp.show()
    sys.exit(app.exec_())