__author__ = 'Scott'

import time

from PySide.QtCore import QThread, SIGNAL


class UpdateDataThread(QThread):
    def __init__(self, serverController):
        QThread.__init__(self)
        self.stopped = False
        self.tool = serverController

    def run(self):
        #initial
        self.tool.fetchServerChat()
        time.sleep(0.5)
        self.emit(SIGNAL('update(QString)'), "done")
        while not self.stopped:
            try:
                self.tool.fetchPlayers()
                self.tool.fetchChat()
                self.tool.fetchInfo()
                self.tool.runTasks()
                self.emit(SIGNAL('update(QString)'), "done")
                time.sleep(2)
            except: #retry a connection
                self.tool.reconnect()

    def stop(self):
        self.stopped = True
