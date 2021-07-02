# Name: Testing
# Description: Testing
# Author: johnscott78
# Era: Any
# Date: Fri Jul 02 2021

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine

def GetTwoMobiles(notorieties = None, maxDistance = -1):
	disallowedNotos = 'Attackable', 

    mobiles = Engine.Mobiles.Where(lambda m: (notorieties == None or notorieties.Contains(m.Notoriety.ToString())) and (maxDistance == -1 or m.Distance < maxDistance) and not InFriendList(m.Serial) and not InIgnoreList(m.Serial) and m.Serial != Engine.Player.Serial).OrderBy(lambda m: m.Distance).Take(2).ToArray()

    return (mobiles[0].Serial, mobiles[1].Serial)

(one, two) = GetTwoMobiles(None, -1)