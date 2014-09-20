__author__ = 'Scott'
import webbrowser

from PySide.QtCore import *
from PySide.QtGui import *


class PlayerView(QTableWidget):
    def __init__(self, parent):
        super(PlayerView, self).__init__(parent)
        self.parent = parent
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.columnNames = ["ID", "Name", "Class", "Kills", "Deaths", "Level", "Score", "Ping", "Player ID", "VIP", "Hero ID", "Team"]
        self.setRowCount(16)
        self.setColumnCount(len(self.columnNames))
        #create table
        for row in range(0,len(self.columnNames)):
            for column in range(0, len(self.columnNames)):
                self.setHorizontalHeaderItem(column,QTableWidgetItem(self.columnNames[column]))
        self.setShowGrid(True)
        #self.setUpdatesEnabled(True)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.setColumnHidden(0, True)
        self.setColumnHidden(8, True)
        self.setColumnHidden(9, True)
        self.setColumnHidden(10, True)
        self.setColumnHidden(11, True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menuHandler)
        #self.customContextMenuRequested.connect(self.tableRightClickMenu)
        playerHeaderView = self.horizontalHeader()
        playerHeaderView.setResizeMode(QHeaderView.Stretch)
        playerHeaderView.setHighlightSections(False)

        self.connect( parent.getDataThread, SIGNAL("update(QString)"), self.updatePlayerTable )

    def updatePlayerTable(self):
        playerArray = self.parent.sc.players
        playerList = []
        rowCount = 0
        if len(playerArray) > 0:
            for player in playerArray:
                tmpList = [player.getId(), player.getName(), player.getKit(), player.getKills(), player.getDeaths(), player.getLevel(), player.getScore(),
                           player.getPing(), player.getPlayerId(), player.isVip(), player.getHeroId(), player.getTeam()]
                playerList.append(tmpList)
            for row in range(0,len(playerList)):
                for column in range(0, len(self.columnNames)):
                    colour = QColor()
                    if playerList[row][11] == "Royal": col = "blue"
                    else: col = "red"
                    self.setHorizontalHeaderItem(column,QTableWidgetItem(self.columnNames[column]))
                    Item = QTableWidgetItem(str(playerList[row][column]))
                    colour.setNamedColor(col)
                    Item.setForeground(QBrush(colour))
                    self.setItem(rowCount, column, Item)
                    if playerList[row][9]:
                        colour.setNamedColor("yellow")
                        Item.setBackground(QBrush(colour))
                rowCount += 1
            self.setRowCount(rowCount)
        else:
            self.setRowCount(0)
        self.resizeRowsToContents()

    def menuHandler(self,pos):
        menu = QMenu()
        warnAction = menu.addAction("Warn")
        kickAction = menu.addAction("Kick")
        makeVipAction = menu.addAction("Make VIP")
        removeVipAction = menu.addAction("Remove VIP")
        viewPlayerAction = menu.addAction("View Player Profile")
        #warnAction.triggered.connect()
        makeVipAction.triggered.connect(self.modifyVipStatus)
        removeVipAction.triggered.connect(lambda: self.modifyVipStatus(remove=True))
        viewPlayerAction.triggered.connect(self.openPlayerProfile)
        menu.exec_(self.mapToGlobal(pos))

    def modifyVipStatus(self, remove=False):
        selected = self.currentRow()
        status = 1
        if remove: status = 0
        if self.item(selected, 1) is not None:
            self.parent.sc.modifyVip(self.item(selected, 1).text(),
                self.item(selected, 8).text(), status)
        self.selectionModel().clearSelection()

    def openPlayerProfile(self):
        selected = self.currentRow()
        if self.item(selected, 1) is not None:
            webbrowser.open("http://www.battlefieldheroes.com/en/player/{0}".format(
                self.item(selected, 8).text()))
        self.selectionModel().clearSelection()


