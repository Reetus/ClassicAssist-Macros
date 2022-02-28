# Name: Recall Miner
# Description: Mines ore recalling through given runebooks. Read instructions
# Author: Kakagriss
# Shard: UOG-Demise
# Date: Mon Feb 28 2022

# Instructions: You will need a runebook with the first rune being your dropoff location, where you should have a container and a forge.
# replace the serials below for these items, as well as for your mining runebooks. You can use as many as you want with as many runes as you want.
# It also needs tinkering for crafting shovels. Mines only the tile to your south!!!. Happy mining!

from Assistant import Engine
	
recallbuttons = [5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95]	
miningresources = [0x19b8, 0x19b7, 0x19b9, 0x19ba, 0x3197, 0x3192, 0x3194, 0x3195, 0x3193, 0x3198]
oreTypes = [0x19b7, 0x19b8, 0x19b9, 0x19ba]
craftGumpId = 0x38920abd
runebooks = [0x4281493c,0x40b3e9f9,0x42814d12] #Replace this with your own runebooks
homebook = 0x40b3e810 #Replace this with your own runebook with dropoff location
resChest = 0x41ca1929 #Replace this with your resource container
forge = 0x40110f44 #Replace this with your forge

def GetRunebookEntries(serial):
    entries = []
    SysMessage(str(serial))
    UseObject(serial)
    if WaitForGump(0x554b87f3, 5000):
        res,gump = Engine.Gumps.GetGump(0x554b87f3)
        
        y = 60
        
        while y <= 165:
            element = gump.Pages[1].GetElementByXY(145, y)
            if element != None and element.Hue != 0:
                entries.append(element.Text)

            y = y + 15
            
        y = 60

        while y <= 165:
            element = gump.Pages[1].GetElementByXY(305, y)
            if element != None and element.Hue != 0:
                entries.append(element.Text)
                
            y = y + 15
            
    return entries
    
def Tinker(category, button):
	count = CountType(0x1bf2, "backpack", 0)
	countcont = CountType(0x1bf2, resChest, 0)
	
	if countcont == 0:
		SysMessage("Out of iron ingots!", 33)
		Stop()
	if count < 50:
		MoveType(0x1bf2, resChest, "backpack", 0, 0, 0, 0, 50)
		Pause(1000)
	if FindType(0x1eb8, 0, "backpack"):
		UseObject("found")	
		ReplyGump(craftGumpId, category)
		WaitForGump(craftGumpId, 5000)
		ReplyGump(craftGumpId, button)
		WaitForGump(craftGumpId, 5000)
	else:
		SysMessage("Out of tinker tools!", 33)
		Stop()
		
def Mine():
	if FindType(0xf39, -1, "backpack") or FindType(0xe86, -1, "backpack"):
		tool = GetAlias("found")
	else:
		SysMessage("Out of mining tools!", 33)
		Stop()
	UseObject(tool)
	WaitForTarget(1000)
	TargetTileOffset(0, 1, 0) #Here mines the tile to your south
	Pause(1000)
		
def DropResources(runebook):
	UseObject(runebook)
	WaitForGump(0x554b87f3, 5000)
	ReplyGump(0x554b87f3, 5)
	Pause(5000)
	for item in miningresources:
		while FindType(item, -1, "backpack"):
			MoveItem("found", resChest)
			Pause(1000)

def SmeltOre(container, object):
	ClearIgnoreList()
	UseObject(container)
	WaitForContents(container, 2000)
	for ore in oreTypes:
		while FindType(ore, -1, container):
			if Graphic('found') == 0x19b7:
				item = Engine.Items.GetItem(GetAlias('found'))
				if item.Count <= 1:
					IgnoreObject('found')
					continue
			UseObject('found')
			WaitForTarget(5000)
			Target(object)
			Pause(1000)
			while FindType(0x1bf2, 3):
				MoveItem('found', container)
				Pause(1000)
				IgnoreObject('found')
			while FindType(0x1bf2, -1, 'backpack'):
				MoveItem('found', container)
				Pause(1000)
				IgnoreObject('found')	
					
for y in range(len(runebooks)):
	currentbook = runebooks[y]
	entries = GetRunebookEntries(currentbook)
	for x in range(len(entries)):
		UseObject(currentbook)
		WaitForGump(0x554b87f3, 5000)
		ReplyGump(0x554b87f3, recallbuttons[x])
		Pause(5000)
		ClearJournal()
		while not InJournal("metal here to mine", "system"):
			Mine()
			if Weight() >= MaxWeight() - 80:
				DropResources(homebook)
				SmeltOre(resChest, forge)
				toolsnumber = CountType(0xf39, "backpack",0)
				tinkernumber = CountType(0x1eb8, "backpack", 0)
				if tinkernumber < 3:
					Tinker(8, 23)
				if toolsnumber < 3:
					Tinker(8, 72)
				UseObject(currentbook)
				WaitForGump(0x554b87f3, 5000)
				ReplyGump(0x554b87f3, recallbuttons[x])
				Pause(5000)