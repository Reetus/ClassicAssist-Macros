# Name: Recall Lumber
# Description: Chops down trees recalling through given runebooks.
# Author: Kakagriss
# Shard: UOG-Demise
# Date: Tue Mar 01 2022

# Instructions: You will need a runebook with the first rune being your dropoff location, where you should have a container.
# replace the serials below for these items, as well as for your lumber runebooks. You can use as many as you want with as many runes as you want.
# you also need to have a hatchet. It doesn't make tools. Chops only the tree to your south!!!. Loop and play. Happy lumbering!

from Assistant import Engine
	
recallbuttons = [5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95]	
lumberresources = [0x1bd7, 0x1bdd, 0x3199, 0x318f, 0x2f5f, 0x3190, 0x3191]
craftGumpId = 0x38920abd
runebooks = [0x428143f6, 0x40b39296] #Replace this with your own runebooks
homebook = 0x40b3f203 #Replace this with your own runebook with dropoff location
resChest = 0x4347925c #Replace this with your resource container

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
    		
def Lumber():
	if not FindLayer("TwoHanded"):
		if FindType(0xf43, -1, "backpack"):
			EquipItem("found", "TwoHanded")
			Pause(1000)
		else:
			SysMessage("Out of lumber tools!", 33)
			Stop()
	UseLayer("TwoHanded")
	WaitForTarget(1000)
	TargetTileOffsetResource(0, 1, 0) #Here chops the tree to your south
	Pause(1000)
		
def DropResources(runebook):
	UseObject(runebook)
	WaitForGump(0x554b87f3, 5000)
	ReplyGump(0x554b87f3, 5)
	Pause(5000)
	for item in lumberresources:
		while FindType(item, -1, "backpack"):
			MoveItem("found", resChest)
			Pause(1000)

def CutLogs():
	while FindType(0x1bdd, -1, "backpack"):
		UseLayer("TwoHanded")
		WaitForTarget(5000)
		Target("found")
		Pause(1000)
					
for y in range(len(runebooks)):
	currentbook = runebooks[y]
	entries = GetRunebookEntries(currentbook)
	for x in range(len(entries)):
		UseObject(currentbook)
		WaitForGump(0x554b87f3, 5000)
		ReplyGump(0x554b87f3, recallbuttons[x])
		Pause(5000)
		ClearJournal()
		while not InJournal("not enough wood here", "system"):
			Lumber()
			if Weight() >= (MaxWeight() - 150) and Weight() <= (MaxWeight() - 80):
				CutLogs()
			if Weight() >= (MaxWeight() - 80):
				CutLogs()
				DropResources(homebook)
				UseObject(currentbook)
				WaitForGump(0x554b87f3, 5000)
				ReplyGump(0x554b87f3, recallbuttons[x])
				Pause(5000)