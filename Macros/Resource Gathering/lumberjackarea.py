# Name: Lumberjack Near Me
# Description: Attempts to chop all trees in a 10x10 area around you
# Author: Bittiez
# Shard: Ruins and Riches
from ClassicAssist.UO.Data import Statics
from ClassicAssist.UO import UOMath
from Assistant import Engine
from System import Convert
import clr
clr.AddReference('System.Core')

# User Config Here ////////////////////////////////////////////////////////////////////
#   _____ ____  _   _ ______ _____ _____
#  / ____/ __ \| \ | |  ____|_   _/ ____|
# | |   | |  | |  \| | |__    | || |  __
# | |   | |  | | . ` |  __|   | || | |_ |
# | |___| |__| | |\  | |     _| || |__| |
#  \_____\____/|_| \_|_|    |_____\_____|
#
#
packAnimals = [0x23e1] # For more than one pack animal use a comma: [0x23e1, 0x23e1]
logs = [0x1be0]        # In case your server has different log types, also use a comma here for multiple
dropLogs = False       # If you want to drop logs instead of placing into pack animals change this to True
moveLogsToPackAnimal = True
#
#
#
#
# End User Config ////////////////////////////////////////////////////////////////////////

packCount = 0 #Do not change from 0
maxPackCnt = len(packAnimals) #Do not change
def GetNearestTree():
    trees = []
    for x in range(Engine.Player.X-10, Engine.Player.X+10):
        for y in range(Engine.Player.Y-10, Engine.Player.Y+10):
            statics = Statics.GetStatics(Convert.ChangeType(Engine.Player.Map, int), x, y)
            if statics == None:
                continue
            for s in statics:
                if s.Name.Contains("tree"):
                    trees.append({'X': s.X, 'Y': s.Y})
    return trees
def moveToPackAnimal():
    global packCount
    pack = packAnimals[packCount]
    for log in logs:
        while FindType(log, -1, 'backpack'):
            MoveItem("found", pack)
            Pause(1000)
    packCount += 1;
    if packCount >= maxPackCnt:
        packCount = 0

def moveToTree(tree):
    i = 0
    while X("self") <> tree['X'] and Y("self") <> tree['Y']:
        if i >= 3:
            HeadMsg("Pathfinding failed. Skipping tree.", "self")
            return False
        HeadMsg("*Pathfinding*", "self")
        Pathfind(tree['X'], tree['Y'], 0)
        Pause(2000)
        i += 1
    return True

def lumberjack():
    while not InJournal("not enough") and not InJournal("can't use an axe"):
        UseLayer("TwoHanded")
        WaitForTarget(1000)
        TargetTileOffsetResource(-1, 0, 0)
        Pause(1100)

        if dropLogs:
            for log in logs:
                while FindType(log, -1, 'backpack'):
                    MoveItemOffset("found", 0, 1, 0, -1)
                    Pause(1000)
        if moveLogsToPackAnimal:
            moveToPackAnimal()

Trees = GetNearestTree()
if len(Trees) > 0:
    TotalTrees = len(Trees)
    SysMessage(str(TotalTrees) + " total trees in queue")
    for tree in Trees:
        tree['X'] += 1
        if moveToTree(tree):
            lumberjack()
            TotalTrees -= 1
            SysMessage(str(TotalTrees) + " trees left in the queue!")
            ClearJournal()
            Msg("all guard me")