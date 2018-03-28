#!/usr/bin/env python
from sys import path
from die import * 
import sys
import crapsResources_rc
from time import sleep
from logging import basicConfig, getLogger, DEBUG, INFO, CRITICAL
from pickle import dump, load
from os import path
from PyQt5.QtCore import pyqtSlot, QCoreApplication, QSettings, QTimer
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

startingBankDefault = 100
maximumBetDefault = 100
minimumBetDefault = 10
logFilenameDefault = 'craps.log'
pickleFilenameDefault = ".crapsSavedObjects.pl"

class Dice(QMainWindow) :
    """A game of Craps."""
    die1 = die2 = None

    def __init__( self, parent=None ):
        """Build a game with two dice."""

        super().__init__(parent)

        self.logger = getLogger("Lindsley.craps")
        self.appSettings = QSettings()
        self.quitCounter = 0 # used in a workaround for a QT5 bug.

        uic.loadUi("Craps.ui", self)
        self.payouts = [0,0,0,0, 2.0, 1.5, 1.2, 0, 1.2, 1.5, 2.0, 0, 0]
        self.pickleFilename = pickleFilenameDefault

        self.restoreSettings()

        if path.exists(self.pickleFilename):
            self.die1, self.die2, self.firstRoll, self.results, self.playerLost, self.firstRollValue,
            self.buttonText, self.wins, self.losses, self.currentBet, self.currentBank = self.restoreGame()
        else:
            self.restartGame()
        self.rollButton.clicked.connect(self.rollButtonClickedHandler)
        self.preferencesButton.clicked.connect(self.preferencesButtonClickedHandler)

        self.bidSpinBox.setRange ( 10, 100 )
        self.bidSpinBox.setSingleStep ( 5 )

             #          0  1  2  3  4    5    6    7    8    9    10   11   12
        self.payouts = [0, 0, 0, 0, 2.0, 1.5, 1.2, 1.0, 1.2, 1.5, 2.0, 1.0, 0]

        self.results = 'Welcome to Craps'
        self.rollButton.clicked.connect(self.rollButtonClickedHandler)
        self.preferencesButton.clicked.connect(self.preferencesButtonClickedHandler)

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
        self.bankValue.setText(str(self.currentBank))

    def restartGame(self):
        self.die1 = Die()
        self.die2 = Die()
        self.die1.setValue(5)
        self.die2.setValue(6)
        self.firstRoll = True
        self.results = ""
        self.playerLost = False
        self.firstRollValue = 0
        self.buttonText = "Roll"
        self.wins = 0
        self.losses = 0
        self.currentBet = 0
        self.currentBank = self.startingBank

    def saveGame(self):
        saveItems = (self.dial, self.die2, self.firstRoll, self.results, self.playerLost, self.firstRollValue,
            self.buttonText, self.wins, self.losses, self.currentBet, self.currentBank)
        if self.appSettings.contains('pickleFilename'):
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFilename',
                type=str)), 'wb') as pickleFile:
                dump(saveItems, pickleFile)
        else:
            self.logger.critical("No pickle Filename")

		# Player asked for another roll of the dice.

        def restoreGame(self):
            if self.appSettings.contains('pickleFilename'):
                self.appSettings.value('pickleFilename', type=str)
                with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFilename', type=str)), 'rb') as pickleFile:
                    return load(pickleFile)
            else:
                self.logger.critical("No pickle Filename")

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

    def restoreSettings(self):
        # Restore settings values, write defaults to any that don't already exist
        if self.appSettings.contains('startingBank'):
            self.startingBank = self.appSettings.value('startingBank', type=int)
        else:
            self.startingBank = startingBankDefault
            self.appSettings.setValue('startingBank', self.startingBank)

        if self.appSettings.contains('maximumBet'):
            self.maximumBet = self.appSettings.value('maximumBet', type=int)
        else:
            self.maximumBet = maximumBetDefault
            self.appSettings.setValue('maximumBet', self.maximumBet)

        if self.appSettings.contains('minimumBet'):
            self.minimumBet = self.appSettings.value('minimumBet', type=int)
        else:
            self.minimumBet = minimumBetDefault
            self.appSettings.setValue('minimumBet', self.minimumBet)

        if self.appSettings.contains("createLogFile"):
            self.createLogFile = self.appSettings.value('createLogFile')
        else:
            self.createLogFile = logFilenameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)

        if self.appSettings.contains('logFile'):
            self.logFilename = self.appSettings.value('logFile', type=str)
        else:
            self.logFilename = 'pythonGraderLog.txt'
            self.appSettings.setValue('logFile', self.logFilename)

        if self.appSettings.contains('pickleFilename'):
            self.pickleFilename = self.appSettings.value('pickleFilename', type=str)
        else:
            self.pickleFilename = ".crapsSavedObjects.pl"
            self.appSettings.setValue('pickleFilename', self.pickleFilename)

    def preferencesButtonClickedHandler(self):
        print("Setting preferences")
        preferencesDialog = PreferencesDialog()
        preferencesDialog.show()
        preferencesDialog.exec_()
        self.restoreSettings()
        self.updateUI()

class PreferencesDialog(QDialog):
    def __init__(self, parent = Dice):
        super(PreferencesDialog, self).__init__()

        uic.loadUi('preferencesDialog.ui', self)

        self.appSettings = QSettings()
        if self.appSettings.contains('startingBank'):
            self.startingBank = self.appSettings.value('startingBank', type=int)
        else:
            self.startingBank = startingBankDefault
            self.appSettings.setValue('startingBank',self.startingBank)

        if self.appSettings.contains('maximumBet'):
            self.maximumBet = self.appSettings.value('maximumBet', type=int)
        else:
            self.maximumBet = maximumBetDefault
            self.appSettings.setValue('maximumBet', self.maximumBet)

        if self.appSettings.contains('minimumBet'):
            self.minimumBet = self.appSettings.value('minimumBet', type=int)
        else:
            self.minimumBet = minimumBetDefault
            self.appSettings.setValue('minimumBet', self.minimumBet)

        # if self.appSettings.contains('createLogFile'):
        #     self.createLogFile = self.appSettings.value('createLogFile', type = bool)
        # else:
        #     self.createLogFile = logFilenameDefault
        #     self.appSettings.setValue('createLogFile', self.createLogFile)

        self.buttonBox.rejected.connect(self.cancelClickedHandler)
        self.buttonBox.accepted.connect(self.okayClickedHandler)
        self.startingBankValue.editingFinished.connect(self.startingBankValueChanged)
        self.maximumBetValue.editingFinished.connect(self.maximumBetValueChanged)
        self.minimumBetValue.editingFinished.connect(self.minimumBetValueChanged)
       # self.createLogFileCheckBox.stateChanged.connect(self.createLogFileChanged)
        self.updateUI()

    def updateUI(self):
        self.startingBankValue.setText(str(self.startingBank))
        self.maximumBetValue.setText(str(self.maximumBet))
        self.minimumBetValue.setText(str(self.minimumBet))

    def startingBankValueChanged(self):
        fred = int(self.startingBankValue.text())
        self.startingBank = int(self.startingBankValue.text())

    def maximumBetValueChanged(self):
        self.maximumBet = int(self.maximumBetValue.text())
    def minimumBetValueChanged(self):
        self.minimumBet = int(self.minimumBetValue.text())

    # @pyqtSlot()
    def okayClickedHandler(self):
        print("Clicked okay button")
        basePath = path.dirname(path.realpath(__file__))
        self.preferencesGroup = (('startingBank', self.startingBank), \
                                 ('maximumBet', self.maximumBet), \
                                 ('minimumBet', self.minimumBet), \
                                 ('createLogFile', self.createLogFile), \
                                 )
        for setting, variableName in self.preferencesGroup:
            # if self.appSettings.contains(setting):
            self.appSettings.setValue(setting, variableName)

        self.close()

        # @pyqtSlot()
    def cancelClickedHandler(self):
        self.close()
if __name__ == "__main__":
    QCoreApplication.setOrganizationName("Jazmine's Stuff");
    QCoreApplication.setOrganizationName("jazminesstuff.com");
    QCoreApplication.setApplicationName("Craps");
    appSettings = QSettings()
    app = QApplication(sys.argv)
    diceApp = Dice()
    diceApp.updateUI()
    diceApp.show()
    sys.exit(app.exec_())


