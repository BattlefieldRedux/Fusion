__author__ = 'Scott'

import time
import re
import queue
import util
import xml.etree.ElementTree as etree

COMMAND_PREFIXES = ["|", "/"]

class AdminTool:
    def __init__(self,server):
        self.server = server
        self.players =[]
        self.chat = []
        self.mods =[]
        self.admins = []
        self.owners = []
        self.q = queue.Queue() #queue to hold actions made from GUI thread, 2 cmd's sent at once means a mess when recieving

        ##config
        self.bannerUrl = ""
        self.maxLevelDiff = 6
        self.balanceGameEnabled = False

        self.afkLog = {}
        self.afkChecked = False #boolean to check only once each round
        self.lastCheck = 0
        self.getStaff()
        #self.loadConfig()



    def fetchPlayers(self):
        self.resetPlayerUpdates()
        new = self.server.getPlayers()
        for p in new:
            player = self.getPlayerWithPlayerId(p.getPlayerId())
            if player is not None:
                player.updateFromPlayer(p)
            else:
                self.players.append(p)
        quitPlayers = self.removeQuitPlayers()
        #TODO log players that have quit

    def calcAverage(self):
        levels = []
        for each in self.players:
            levels.append(int(each.getLevel()))
        self.averageLevel = util.median(levels)

    def fetchChat(self):
        self.chat = self.server.getClientChatBuffer()
        ##run any commands in chat
        for each in self.chat:
            msg = each[5]
            if msg[0] in COMMAND_PREFIXES:
                player = self.getPlayerWithId(each[0])
                if player is not None: self.runCommand(msg, player)

    def fetchServerChat(self):
        self.chat = self.server.getServerChatBuffer()

    def fetchInfo(self):
        self.server.getServerInfo()

    def adminSay(self, msg):
        self.q.put(lambda: self.server.adminSay(msg))

    def balanceGame(self):
        if not self.isPregame():
            for p in self.players:
                if int(p.getLevel()) > self.averageLevel+self.maxLevelDiff:
                    self.server.kickPlayer(p.getId(), "Balance - Level too high")

    def reconnect(self):
        try:
            while not self.server.connect():
                time.sleep(15)
        except:
            pass

    def runTasks(self):
        #self.checkAFKPlayers()
        self.calcAverage()
        if self.balanceGameEnabled:
            self.balanceGame()
        while not self.q.empty():
            cmd = self.q.get()
            cmd()


    def isMod(self, player):
        return player.getPlayerId() in self.mods or player.getPlayerId() in self.admins or player.getPlayerId() in self.owners

    def isAdmin(self, player):
        return player.getPlayerId() in self.admins or player.getPlayerId() in self.owners

    def isOwner(self, player):
        return player.getPlayerId() in self.owners

    def checkAFKPlayers(self):
        """
        Method to try and kick AFK players from the TE game mode ONLY to stop stat padding
        Work in progress...
        """
        playersDead = self.arePlayersAllDead()
        if self.server.mode == "gpm_cdm" and self.isEndRound() and not self.isPregame() and not self.afkChecked:
            print("check")
            #only way to check if round is not ongoing is if all players are dead
            for p in self.players:
                if int(p.getLevel()) == -1: continue
                #now check which players have a score of 0 or a score divisible by 1000
                score = int(p.getScore())
                name = p.getName()
                if (score == 0 or score%1000 == 0) and int(p.getKills()) == 0:
                        #self.server.kickPlayer(p.getId(), "AFK")
                        print("kicked " + p.getPlayerName())
            self.afkChecked = True
        else:
            #at least 1 min before checks
            if playersDead and time.time()-self.lastCheck > 60: #dont check twice in 1 round
                self.afkChecked = False
        print(self.afkLog)



    def arePlayersAllDead(self):
        if len(self.players) == 0:
            return False
        for p in self.players:
            if p.isAlive():
                return False
        return True

    def isEndRound(self):
        return self.server.natTickets == 0 or self.server.royTickets == 0

    def getPlayerWithName(self, name):
        for p in self.players:
            if p.getName() == name:
                return p
        return None

    def getPlayerWithId(self, search):
        count = 0
        while count < len(self.players):
            if search == self.players[count].getId():
                return self.players[count]
            count += 1
        return None

    def getPlayerWithPlayerId(self, search):
        count = 0
        while count < len(self.players):
            if search == self.players[count].getPlayerId():
                return self.players[count]
            count += 1
        return None

    def isPregame(self):
        return self.server.roySize < 2 or self.server.natSize < 2

    def searchByName(self, search):
        "search = name:str"
        search = re.escape(search.lower())
        regex = "^{}".format(search)
        Found = False
        count = 0
        while not Found and count < len(self.players):
            if re.match(regex, self.players[count].getName().lower()) is not None:
                return self.players[count]
            count += 1
        return None

    def resetPlayerUpdates(self):
        for p in self.players:
            p.updated = False

    def removeQuitPlayers(self):
        quitPlayers = [p for p in self.players if not p.updated]
        self.players = [p for p in self.players if p.updated]
        return quitPlayers


    def getStaff(self):
        try:
            with open("staff.txt", mode="r",encoding="utf-8") as my_file:
                for line in my_file:
                    line = line.split(",")
                    if int(line[1]) == 1:
                        self.mods.append(line[0])
                    elif int(line[1]) == 2:
                        self.admins.append(line[0])
                    elif int(line[1]) == 1337:
                        self.owners.append(line[0])
        except IOError:
            pass

    def addStaff(self, playerid, level):
        try:
            with open("staff.txt", mode="a",encoding="utf-8") as my_file:
                my_file.write("{},{}\n".format(playerid, level))
        except IOError:
            pass

    def getRealNameFromShort(self, short): #short to long
        mapNames = {"BB":"lake", "SS":"seaside_skirmish", "CC":"smack2", "VV":"village", "LL":"lunar",
                    "AA":"woodlands", "WW":"wicked_wake", "SS2":"mayhem", "II":"Dependant_Day",
                    "BBN":"lake_night", "BBS":"lake_snow", "RR":"royal_rumble", "VVS":"village_snow",
                    "CCN":"smack2_night", "MM":"ruin", "FF":"river", "SSN":"seaside_skirmish_night"} #TODO-add more map names
        if short in mapNames:
            return mapNames[short]
        else:
            return None

    def modifyVip(self, name, playerId, status):
        #queue the function
        self.q.put(lambda: self.server.setVipStatus(name, playerId, status))

    def runCommand(self, cmd, player):
        full = cmd.split()
        command = full[0]
        command = command[1:]
        args = full[1:]

        if command == "w" and self.isMod(player):
            aim = args[0]
            arg = " ".join(args[1:])
            arg += " [{}]".format(player.getName())
            name = self.searchByName(aim)
            if name is not None:
                self.server.warnPlayer(name.getName(), arg)
            else:
                self.server.privateToPlayer("Player not found.", player.getId())

        elif command == "k" and self.isMod(player):
            aim = args[0]
            arg = " ".join(args[1:])
            arg += " [{}]".format(player.getName())
            p = self.searchByName(aim)
            if p is not None:
                self.server.kickPlayer(p.getId(), arg)

        elif command == "s" and self.isMod(player):
            self.server.adminSay("{} [{}]".format(args, player.getName()))

        elif command == "rm" and self.isMod(player):
            self.server.restartMap()

        elif command == "b" and self.isAdmin(player):
            aim = self.searchByName(args[0])
            reason = args[1]
            self.server.ban(aim.getName(), reason, player.getName())

        elif command == "jump" and self.isMod(player):
            mapName = self.getRealNameFromShort(args[0])
            if mapName is not None: self.server.jumpToMap()

        elif command == "deaths":
            self.server.privateToPlayer(player.getId(), ": DEATHS - {}".format(player.getDeaths()))

        elif command == "p":
            to = self.searchByName(args[0])
            if to is not None:
                msg = args[1]
                self.server.privateToPlayerName(to.getName(),"PM from {}: {}".format(player.getName(), msg))

        elif command == "addvip" and self.isAdmin(player):
            aim = self.searchByName(args[0])
            if aim is not None:
                self.server.setVipStatus(aim.getName(), aim.getPlayerId(), 1)
                self.server.privateToPlayerName(player.getName(), aim.getName() + " added as VIP.")
                self.server.privateToPlayerName(aim.getName(), "You've been made a VIP!")
            else: self.server.privateToPlayerName("Player not found.")

        elif command == "delvip" and self.isAdmin(player):
            aim = self.searchByName(args[0])
            if aim is not None:
                self.server.setVipStatus(aim.getName(), aim.getPlayerId(), 0)
                self.server.privateToPlayerName(player.getName(), aim.getName() + " removed as VIP.")
                self.server.privateToPlayerName(aim.getName(), "You're VIP status has been revoked!")
            else:
                self.server.privateToPlayerName("Player not found.")

        elif command == "addmod" and self.isAdmin(player):
            aim = self.searchByName(args[0])
            if aim is not None:
                self.addStaff(aim.getPlayerId(), 3)
                self.server.privateToPlayerName(player.getName(), aim.getName() + " added as MOD.")
            else:
                self.server.privateToPlayerName("Player not found.")

        elif command == "addadmin" and self.isAdmin(player):
            aim = self.searchByName(args[0])
            if aim is not None:
                self.addStaff(aim.getPlayerId(), 4)
                self.server.privateToPlayerName(player.getName(), aim.getName() + " added as MOD.")
            else:
                self.server.privateToPlayerName("Player not found.")

        elif command == "vips":
            vipList = []
            for each in self.players:
                if each.isVip(): vipList.append(each.getName())
            if len(vipList) > 0:
                vips = "VIPs: " + ", ".join(vipList)
            else: vips = "No VIPs are online right now."
            self.server.privateToPlayerName(player.getName(), vips)

        elif command == "staff":
            modList = []
            for each in self.players:
                if self.isMod(each) or self.isAdmin(each) or self.isOwner(each): modList.append(each.getName())
            if len(modList) > 0:
                staff = "Staff: " + ", ".join(modList)
            else: staff = "No staff online."
            self.server.privateToPlayerName(player.getName(), staff)

        elif command == "ping":
            self.server.privateToPlayer(player.getId(), ": PING - {}".format(player.getPing()))



