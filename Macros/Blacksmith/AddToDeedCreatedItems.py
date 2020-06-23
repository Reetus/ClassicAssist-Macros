# Name: Add to deed created items
# Description: Search and add items corresponding to prompted deed. Gumps for deed may vary in different shards.
# Author: Aru
# Era: Any

import clr
import System
clr.AddReference('System.Core')
clr.ImportExtensions(System.Linq)
from Assistant import Engine

def GetBackpackItems(filter = None):
    if Engine.Player == None:
        return []
    SysMessage("checking")

    if Engine.Player.Backpack.Container == None:
        UseObject('backpack')
        WaitForContents('backpack', 5000)

    items = Engine.Player.Backpack.Container.SelectEntities(lambda i: filter == None or i.Name.Contains(filter))

    if (items == None):
        return []

    return items.Select(lambda i: i.Serial)

def GetLastProperty(serial):
    item = Engine.Items.GetItem(serial)

    if (item == None or item.Properties == None):
        return '';

    return item.Properties[item.Properties.Length-1].Text


PromptAlias('deed')
serial = GetAlias('deed')

deedGoal = GetLastProperty(serial).split(":")[0]

SysMessage(deedGoal)

backpackfoundList = GetBackpackItems(deedGoal)

UseObject('deed')
WaitForGump(0x5afbd742, 6000)

for x in backpackfoundList:
    ReplyGump(0x5afbd742, 2)
    WaitForTarget(6000)
    Target(x)
    SysMessage("Adding item to deed")
    Pause(200)
