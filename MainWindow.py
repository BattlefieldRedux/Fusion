import sys

__author__ = 'Scott'

from PlayerView import *
from UpdateDataThread import *
from AdminTool import *
from ChatView import *
from InfoView import *
from bfhrcon.BFHServer import *
import xml.etree.ElementTree as etree

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.setWindowTitle("Fusion")
        self.connectServer()
        self.playerLayout()
        self.getDataThread.start()

    def connectServer(self):
        ip = ""
        port = 12345
        passw = ""
        try:
            tree = etree.parse('conf/config.xml')
            root = tree.getroot()
            ip = root.find('ip').text
            port = int(root.find('port').text)
            passw = root.find('pass').text
        except IOError:
            print("ERROR: File could not be opened/read.")
            sys.exit(1)
        server = BFHServer(ip,port,passw)
        if len(ip) < 7 or not server.connect():
            print("Problem with server connection or server details provided")
            sys.exit(1)
        self.sc = AdminTool(server)
        self.getDataThread = UpdateDataThread(self.sc)


    def playerLayout(self):
        self.resize(900,620)
        layout = QVBoxLayout()
        layout.addWidget(InfoView(self))
        layout.addWidget(PlayerView(self))

        ##playerchat
        self.chatView = ChatView(self)
        layout.addWidget(self.chatView)

        ##controls
        self.adminSayLineEdit = QLineEdit()
        self.adminSayButton = QPushButton("Admin Say")
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.adminSayLineEdit)
        controlLayout.addWidget(self.adminSayButton)
        layout.addLayout(controlLayout)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(layout)
        self.setCentralWidget(self.mainWidget)

        self.adminSayButton.clicked.connect(self.adminSayAction)


    def adminSayAction(self):
        self.sc.adminSay(self.adminSayLineEdit.text())
        self.adminSayLineEdit.setText("")



if __name__ == "__main__":
    application = QApplication(sys.argv)
    application.setStyle(QStyleFactory.create("cleanlooks")) #sets style of window
    window = mainWindow()
    window.show()
    window.raise_()
    application.exec_()
    sys.exit()


