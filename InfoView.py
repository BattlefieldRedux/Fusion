__author__ = 'Scott'
from PySide.QtCore import *
from PySide.QtGui import *

class InfoView(QWidget):
    def __init__(self, parent):
        super(InfoView, self).__init__(parent)
        layout = QHBoxLayout()
        self.parent = parent
        #self.serverName = QLabel("", self)
        self.currentMap = QLabel("Current Map: SS", self)
        self.currentMap.setAlignment(Qt.AlignLeft)
        self.nextMap = QLabel("Next Map: BB", self)
        self.nextMap.setAlignment(Qt.AlignRight)
        #self.round = QLabel("Round: 1/3", self)
        self.natTickets = QLabel("<font color='red'>50</font>", self)
        self.royTickets = QLabel("<font color='blue'>50</font>", self)
        self.royTickets.setAlignment(Qt.AlignCenter)
        self.natTickets.setAlignment(Qt.AlignCenter)
        #self.avgLevel = QLabel("Avg. Level: 0", self)
        #layout.addWidget(self.serverName)
        layout.addWidget(self.currentMap)
        layout.addWidget(self.natTickets)
        layout.addWidget(self.royTickets)
        layout.addWidget(self.nextMap)
        #layout.addWidget(self.round)
        #layout.addWidget(self.tickets)
        #layout.addWidget(self.avgLevel)
        self.setLayout(layout)

        self.connect(parent.getDataThread, SIGNAL("update(QString)"), self.updateInfo)

    def updateInfo(self):
        #self.serverName.setText(self.parent.sc.name)
        self.currentMap.setText("Current Map: {}".format(self.parent.sc.server.mapName))
        self.nextMap.setText("Next Map: {}".format(self.parent.sc.server.nextMap))
        #self.round.setText("Round: {}/{}".format(self.parent.sc.currentRound, self.parent.sc.roundsPerMap))
        self.natTickets.setText("<font color='red'>{}</font>".format(self.parent.sc.server.natTickets))
        self.royTickets.setText("<font color='blue'>{}</font>".format(self.parent.sc.server.royTickets))
        #self.avgLevel.setText("Avg. Level: {}".format(int(round(self.parent.sc.averageLevel))))

