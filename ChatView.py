__author__ = 'Scott'
from PySide.QtCore import *
from PySide.QtGui import *

class ChatView(QListWidget):
    def __init__(self, parent):
        super(ChatView, self).__init__(parent)
        self.parent = parent
        ##view
        self.setSelectionMode(QListView.NoSelection)
        self.setUniformItemSizes(True)
        #self.setMinimumWidth(490)

        self.connect(parent.getDataThread, SIGNAL("update(QString)"), self.updateChat)

    def updateChat(self):
        #TODO chat can grow an infinite size, need to clear some items when it gets too big
        chat = self.parent.sc.chat
        chat.reverse()
        count = 0
        for each in chat:
            colour = QColor()
            newItem = QListWidgetItem()
            newItem.setText("{0} {1} {2}: {3}".format(each[3], each[4], each[1], each[5]))
            self.insertItem(count, newItem)
            count += 1
            if each[3] == "ServerMessage":
                colour.setNamedColor("darkGreen")
                newItem.setForeground(colour)
            elif each[2] == "1":
                colour.setNamedColor("red")
                newItem.setForeground(colour)
            elif each[2] == "2":
                colour.setNamedColor("blue")
                newItem.setForeground(colour)

