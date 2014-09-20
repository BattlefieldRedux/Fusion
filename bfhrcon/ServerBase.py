__author__ = 'Scott Davey'

"""
Base for connecting and querying BFH/BFP4F/BF2 servers using RCON.
Copyright (C) 2013  Scott Davey, www.sd149.co.uk

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import socket
import hashlib

class ServerBase:
    """server object for BFH/BFP4F servers..."""
    def __init__(self, ip, port, password):
        self.socket = ""
        self.ip = ip
        self.port = int(port)
        self.password = password
        self.version = 0.0

    def __sendFlag(self, c):
        """
        Sends to server including a flag so we can tell when the group of data has ended
        """
        c = "\2"+c+"\n"
        self.socket.send(c.encode("utf-8"))

    def __send(self, c):
        """
        Sends to server
        """
        c += "\n"
        self.socket.send(c.encode("utf-8"))

    def __recvFlag(self, raw=True):
        """
        Made for recieving large amount of data from server, recieves data until end of reply has been reached.
        returns str
        """
        result = self.__bytesToString(self.socket.recv(512))
        while result[-3:] != "x04":
            moreData = self.__bytesToString(self.socket.recv(512))
            result += moreData
        if raw:
            return result[:-4]
        else:
            return result[:-4].replace("\\t", "\t").replace("\\r", "\n").replace("\\n", "\n")

    def __recv(self, raw=True):
        """
        Collect data from last request
        returns str
        """
        return self.__bytesToString(self.socket.recv(256), raw)

    def __bytesToString(self, string, raw=True):
        """
        Using .decode() removes characters needed to use some data returned and to detect the end of a servers reply
        therefore using str() function instead and slicing b'...' away.
        returns str
        """
        if raw:
            string = str(string)
            return string[2:-1]
        else:
            return string.decode()

    def query(self, command, multi=False, raw=True):
        """
        Query the server with an RCON command, set multi to True if there is a large amount of data
        command: String, excluding linebreak
        multi: Bool, used for receiving multiple packets
        returns str
        """
        if not multi:
            self.__send(command)
            return self.__recv(raw)
        else:
            self.__sendFlag(command)
            return self.__recvFlag(raw)

    def connect(self):
        """
        Connects to a BFH server
        Declares the socket, and sets value for modmanager version on server
        Returns reply from server
        """
        mySocket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.socket = mySocket
        self.socket.connect ( (self.ip, self.port) )
        msg = self.socket.recv(128).decode("utf-8") #welcome message, unusued
        self.version = float(msg[-5:-2])
        digest = self.socket.recv(128).decode("utf-8")
        digest = digest[17:33]
        key = digest + self.password
        key = md5(key)
        login = 'login {0}\n'.format(key)
        login = login.encode("utf-8")
        self.socket.send(login)
        msg = mySocket.recv(100).decode("utf-8")
        if msg != "Authentication successful, rcon ready.\n":
            return False
        return True

    def close(self):
        """
        Closes the socket
        """
        self.socket.close()

def md5(dig):
    md5 = hashlib.md5() #make a new md5 object
    dig = dig.encode("utf-8") #coverting string to bytes
    key = md5.update(dig) #md5'ing it all
    key = md5.hexdigest()
    key = str(key)
    return key
