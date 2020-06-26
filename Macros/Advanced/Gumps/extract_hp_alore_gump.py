# Name: Animal Lore Gump HP
# Description: Use gump parser to extract hp / maxhp from animal lore gump
# Author: Reetus
# Shard: OSI

from Assistant import Engine
import re

def GetLoreGumpHP():
    if not GumpExists(0x1db):
        return (0, 0)
    
    res,gump = Engine.Gumps.GetGump(0x1db)
    element = gump.Pages[1].GetElementByXY(180,92)
    
    if element == None:
        return (0, 0)
    
    matches = re.match('.*>(\d+)/(\d+)<.*', element.Text)
    
    if matches == None:
        return (0, 0)
        
    hp = int(matches.group(1))
    maxhp = int(matches.group(2))
    
    return (hp, maxhp)

(hp, maxhp) = GetLoreGumpHP()

HeadMsg(str(hp) + ' / ' + str(maxhp), 'self')
