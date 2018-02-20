#!/usr/bin/env python

from die import * 
import sys
import crapsResources_rc
from time import sleep
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication

class Craps(QMainWindow) :
    """A game of Craps."""
    die1 = die2 = None

    def __init__( self, parent=None ):
        """Build a game with two dice."""

        super().__init__(parent)
        uic.loadUi("Craps.ui", self)

        self.bidSpinBox.setRange ( 10, 100 )
        self.bidSpinBox.setSingleStep ( 5 )

        self.die1 = Die()
        self.die2 = Die()
        self.firstRoll = True
        self.point = 0
        self.results = ""
        self.wins = 0
        self.losses = 0
        self.bank = 100
        self.buttonText = "Roll"

             #          0  1  2  3  4    5    6    7    8    9    10   11   12
        self.payouts = [0, 0, 0, 0, 2.0, 1.5, 1.2, 1.0, 1.2, 1.5, 2.0, 1.0, 0]

        self.results = 'Welcome to Craps'
        self.rollButton.clicked.connect(self.rollButtonClickedHandler)

    def __str__( self ):
        """String representation for Dice.
        """

        return "Die1: %s\nDie2: %s" % ( str(self.die1),  str(self.die2) )

    def updateUI ( self ):
        print("Die1: %i, Die2: %i" % (self.die1.getValue(),  self.die2.getValue()))
        self.die1View.setPixmap(QtGui.QPixmap( ":/" + str( self.die1.getValue() ) ) )
        self.die2View.setPixmap(QtGui.QPixmap( ":/" + str( self.die2.getValue() ) ) )
        # Add your code here to update the GUI view so it matches the game state.
        self.resultsLabel.setText(self.results)
        self.winsLabel.setText(str(self.wins))
        self.lossesLabel.setText(str(self.losses))
        self.bankValue.setText(str(self.bank))

		# Player asked for another roll of the dice.
    def rollButtonClickedHandler ( self ):
        self.currentBet = self.bidSpinBox.value()
        # Play the first roll
        totalRoll = self.die1.roll() + self.die2.roll()
        self.results = 'Roll = {0}'.format(totalRoll)
        if self.firstRoll == True:
            if totalRoll in [7, 11]:
                self.results = "Shooter Wins, Pass Bets Win!"
                self.wins += 1
                self.bank += self.payouts[totalRoll] * self.currentBet
            elif totalRoll in [2, 3, 12]:
                self.results = "Shooter Loses, Don't Pass Bets Win!"
                self.losses += 1
                self.bank -= self.payouts[totalRoll] * self.currentBet
            else:
                self.point = totalRoll
                self.results = 'Point = {0}'.format(self.point)
                self.firstRoll = False
        else:
            if totalRoll == self.point:
                self.results = "Shooter Wins, Pass Bets Win!"
                self.wins += 1
                self.bank += self.payouts[totalRoll] * self.currentBet
            else:
                self.results = "Shooter Loses, Don't Pass Bets Win!"
                self.losses += 1
                self.bank -= self.payouts[totalRoll] * self.currentBet
            self.firstRoll = True
        self.updateUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    diceApp = Craps()
    diceApp.updateUI()
    diceApp.show()
    sys.exit(app.exec_())


