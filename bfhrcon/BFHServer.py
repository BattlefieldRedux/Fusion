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

from .ServerBase import *
from .Player import *

class BFHServer(ServerBase):
    """
    Adds methods for interacting with a BFH server
    """
    def __init__(self, ip, port, password):
        ServerBase.__init__(self,ip, port, password)

        self.name = ""
        self.mod = ""
        self.ranked = 0
        self.autobalance = 0
        self.reserved = ""
        self.mapName = ""
        self.nextMap = ""
        self.mapMode = ""
        self.currentPlayers = 0
        self.maximumPlayers = 0
        self.joiningPlayers = 0
        self.natTickets = 0
        self.natSize = 0
        self.royTickets = 0
        self.roySize = 0
        self.timeElapsed = 0
        self.roundsPerMap = 0
        self.currentRound = ""
        self.averageLevel = 0
        self.mode = ""


    def isRanked(self):
        r = self.query("exec sv.ranked")
        if r == "0": return False
        return True

    def setRanked(self, ranked):
        self.query("exec sv.ranked {}".format(ranked))

    def getServerName(self):
        return self.query("exec sv.serverName")

    def setServerName(self, name):
        self.query("exec sv.serverName {}".format(name))

    def getPassword(self):
        return self.query("exec sv.password")

    def setPassword(self, passw):
        self.query("exec sv.password {}".format(passw))

    def getServerHost(self):
        return self.query("exec. sv.serverCommunity")

    def getWelcomeMessage(self):
        return self.query("exec sv.welcomeMessage")

    def setWelcomeMessage(self, wel):
        self.query("exec sv.welcomeMessage {}".format(wel))

    def getStartDelay(self):
        return self.query("exec sv.startDelay")

    def setStartDelay(self, st):
        """st: int (seconds)"""
        self.query("exec sv.startDelay {}".format(st))

    def getEndDelay(self):
        return self.query("exec sv.endDelay")

    def setEndDelay(self, en):
        """en: int (seconds)"""
        self.query("exec sv.endDelay {}".format(en))

    def getTicketRatio(self):
        return self.query("exec sv.ticketRatio")

    def setTicketRatio(self, tickets):
        self.query("exec sv.ticketRatio {}".format(tickets))

    def getRoundsPerMap(self):
        return self.query("exec sv.roundsPerMap")

    def getBannerURL(self):
        return self.query("exec sv.bannerURL")

    def setBannerURL(self, banner):
        self.query("exec sv.bannerURL {}".format(banner))

    def getPlayers(self):
        """
        Returns players current in-game.
        returns: tuple of Player objects
        """
        result = self.query("bf2cc pl", True)
        result = result.split("\\r")
        playersList = []
        for each in result:
            playerList = each.split("\\t")
            playersList.append(playerList)
        playersList.pop(-1) #Ended with \\t, so creates empty item, removing it
        currentPlayers = []
        for each in playersList:
            currentPlayers.append(Player(each[0], each[1], each[34], each[4], each[8], each[31],
                each[36], each[30], each[2], each[39], each[37], each[3], each[18], each[47], each[46], each[10]))
        return tuple(currentPlayers)

    def getClientChatBuffer(self):
        """
        Get's new chat, only returns chat that hasn't been recieved already. So this can be called again
        and again, no need to check for repeats.
        returns: A list of tuples.
        """
        allChat = []
        chat = self.query('bf2cc clientchatbuffer', True)
        chat = chat.split("\\r\\r")
        chat.pop(-1) #empty element created at end of list, remove it
        for each in chat:
            chatList = tuple(each.split("\\t"))
            allChat.append(chatList)
        return allChat

    def getServerChatBuffer(self):
        allChat = []
        chat = self.query('bf2cc serverchatbuffer', True)
        chat = chat.split("\\r\\r")
        chat.pop(-1) #empty element created at end of list, remove it
        for each in chat:
            chatList = tuple(each.split("\\t"))
            allChat.append(chatList)
        return allChat

    def getServerInfo(self):
        """
        Returns information about the server
        returns: tuple
        """
        data = self.query('bf2cc si', True).replace("\\n", "").split("\\t")
        if len(data) > 0:
            self.name = data[7]
            self.mod = data[21]
            self.ranked = data[25]
            self.autobalance = data[24]
            self.reserved = data[29]
            self.mapName = data[5]
            self.nextMap = data[6]
            self.mapMode = data[20]
            self.currentPlayers = int(data[3])
            self.maximumPlayers = int(data[2])
            self.joiningPlayers = int(data[4])
            self.natTickets = int(data[11])
            self.natSize = int(data[26])
            self.mode = data[20]
            self.royTickets = int(data[16])
            self.roySize = int(data[27])
            self.timeElapsed = data[18]
            self.roundsPerMap = data[30]
            self.currentRound = data[31]

    def warnPlayer(self, player, msg):
        """
        Warning a player, does not use the proper warning method as it does not
        show correctly in-game. Making use of admin say instead.
        player: str (must be full name, this method will not auto-complete it for you)
        msg: str
        returns: str
        """
        return self.query('exec game.sayAll "WARN: {0} REASON: {1}"'.format(player, msg))

    def kickPlayer(self, player, reason):
        """
        Kicks a player from server.
        player: str
        reason: str
        returns: str
        """
        return self.query('kick {0} "{1}"'.format(player, reason))

    def adminSay(self, msg):
        """
        Displays a message in yellow text on left side of players screen
        :param msg: string
        :return: string (response from server)
        """
        return self.query('exec game.sayAll ": {}"'.format(msg))

    def setVipStatus(self, player, playerID, status):
        """
        :param player: player name - str
        :param playerID: the account id, not hero id
        :param status: a 1 if adding vip, 0 if removing vip
        :return: str (response from server)
        """
        return self.query('exec game.setPersonaVipStatus {} {} {}'.format(player, playerID, status))

    def privateToPlayer(self, pid, msg):
        return self.query('exec game.sayToPlayerWithId {0} "{1}"'.format(pid, msg))

    def privateToPlayerName(self, name, msg):
        return self.query('exec game.sayToPlayerWithName {} "{}"\n'.format(name, msg))

    def privateKick(self, player):
        """
        Kicks a player without anyone knowing about it!
        player: str - can be a name or there ingame ID (1-16)
        """
        return self.query('exec admin.kickPlayer {0}'.format(player))

    def restartMap(self):
        return self.query('exec admin.restartMap')

    def ban(self, player, reason, by):
        return self.query('banby {0} {1} Perm "{2}"'.format(player, by, reason))

    def tempBan(self, player, time, reason, by):
        return self.query('banby {0} {1} {2} "{3} [TempBan]"'.format(player, by, time, reason))

