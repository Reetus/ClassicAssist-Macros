# Name: Smelt all items by prompted type
# Description: Search and smelt all items (by type) from backpack. Uses prompt for get item type. Change {hammer_name} to current name in shard of hammer. Gumps may vary in other shards.
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

def GetFirst(l):
    for item in l:
        return item

PromptAlias('typeToSmelt')
serial = GetAlias('typeToSmelt')

tmpItem = Engine.Items.GetItem(serial)

toSmeltList = GetBackpackItems(tmpItem.Name)
hammerList = GetBackpackItems("{hammer_name}")

hammer = GetFirst(hammerList)

SysMessage("Hammer serial: " + hex(hammer))

UseObject(hammer)
WaitForGump(0x1cc, 5000)

for x in toSmeltList:
	ReplyGump(0x1cc, 14)
	WaitForTarget(5000)
	Target(x)
	SysMessage("Smelting")
	Pause(200)
