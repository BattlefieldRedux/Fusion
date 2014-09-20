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

class Player:
    """
    Representing a player, includes other options for admin tools with their own built in permissions.
    _id: int
    name: str
    kit: str
    kills: int
    deaths: int
    suicides: int
    team: int
    level: int
    score: int
    ping: int
    ip: str
    playerid: int
    vip: int
    heroid: int
    mod: bool, false by default
    admin: bool, false by default
    owner: bool, false by default
    """
    def __init__(self, _id, name, kit, connected, alive, kills, deaths, suicides, team, level, score, ping, ip, playerid, vip, heroid, mod=False, admin=False, owner=False):
        self.__id = _id
        if alive == "1": self.__alive = True
        else: self.__alive = False
        self.__name = name
        if kit == "NA_Gunner_kit" or kit == "RA_Gunner_kit":
            self.__kit = "Gunner"
        elif kit == "RA_Soldier_kit" or kit == "NA_Soldier_kit":
            self.__kit = "Soldier"
        elif kit == "RA_Commando_kit" or kit == "NA_Commando_kit":
            self.__kit = "Commando"
        elif kit == "none":
            self.__kit = "Dead"
        if connected == "1": self.__connected = True
        else: self.__connected = False
        self.__kills = kills
        self.__deaths = deaths
        self.__suicides = suicides
        if int(team) == 1:
            self.__team = "National"
        else:
            self.__team = "Royal"
        self.__level = level
        self.__score = score
        self.__ping = ping
        self.__ip = ip
        self.__playerid = playerid
        if int(vip) == 1:
            self.__vip = True
        else:
            self.__vip = False
        self.__heroid = heroid

    def getId(self):
        return self.__id
    def getName(self):
        return self.__name
    def isAlive(self):
        return self.__alive
    def getKit(self):
        return self.__kit
    def isConnected(self):
        return self.__connected
    def getKills(self):
        return self.__kills
    def getDeaths(self):
        return self.__deaths
    def getSuicides(self):
        return self.__suicides
    def getTeam(self):
        return self.__team
    def getLevel(self):
        return self.__level
    def getScore(self):
        return self.__score
    def getPing(self):
        return self.__ping
    def getIp(self):
        return self.__ip
    def getPlayerId(self):
        return self.__playerid
    def isVip(self):
        return self.__vip
    def getHeroId(self):
        return self.__heroid




