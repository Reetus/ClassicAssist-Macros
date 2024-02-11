# Name: Circuit Trap Solver
# Description: Solves the 'Circuit Trap Training Kit' by checking the gump elements for available moves, remembering successful ones, and removing failed moves from available moves, only tested on UOAlive
# Author: Reetus
# Shard: UOAlive
# Date: Sun Feb 11 2024

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine

gumpID = 0xd04c03da
trap = 0x40276467

def getAvailableMoves():
    moves = []
    [res, gump] = Engine.Gumps.GetGump(gumpID)
    if res:
        dot = gump.GumpElements.FirstOrDefault(lambda g: g.ElementID == 5032)
        rightEle = gump.GetElementByXY(dot.X + 32, dot.Y - 8)
        canGoRight = rightEle != None and (rightEle.ElementID == 9720 or rightEle.ElementID == 2472)
        
        downEle = gump.GetElementByXY(dot.X - 8, dot.Y + 32)  
        canGoDown = downEle != None and (downEle.ElementID == 9720 or downEle.ElementID == 2472)
        
        upEle = gump.GetElementByXY(dot.X - 8, dot.Y - 48)
        canGoUp = upEle != None and upEle.ElementID == 9720
        
        leftEle = gump.GetElementByXY(dot.X - 48, dot.Y - 8)
        canGoLeft = leftEle != None and leftEle.ElementID == 9720
        
        if canGoRight:
            moves.append(2)
        if canGoDown:
            moves.append(3)
        if canGoLeft:
            moves.append(4)
        if canGoUp:
            moves.append(1)
            
    return moves

successMoves = []
failMoves = []

while True:
    ClearJournal()
    if not GumpExists(gumpID):
        while not TargetExists():
            UseSkill('Remove Trap')
            WaitForTarget(100)
        Target(trap)
        WaitForGump(gumpID, 5000)
        print successMoves
        for i in successMoves:
            ReplyGump(gumpID, i)
            WaitForGump(gumpID, 2000)
            
    moves = getAvailableMoves()
    nextMove = moves.FirstOrDefault(lambda i: i not in failMoves)
    print nextMove
    ReplyGump(gumpID, nextMove)
    if not WaitForGump(gumpID, 2000):
        if InJournal("successfully disarm the trap"):        
            break
        failMoves.append(nextMove)
    else:
        successMoves.append(nextMove)
        failMoves = []
        