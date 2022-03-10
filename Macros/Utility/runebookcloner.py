# Name: Runebook Cloner
# Description: Clones given runebook in one or more blank books.
# Author: Kakagriss
# Shard: UOG-Demise
# Date: Mon Mar 07 2022

# Instructions: You will need runes in your backpack and a container with at least one empty runebook. Happy cloning!

from Assistant import Engine

recallbuttons = [5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95]
blankbooks = []

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

def GetItemsInContainer(container):
	items = []
	
	cont = Engine.Items.GetItem(container)
	
	if cont == None:
		print 'Cannot find container'
		return
		
	if cont.Container == None:
		WaitForContents(container, 5000)
		
	for item in cont.Container.GetItems():
		items.append(item.Serial)	
	
	return items
	
def GetRunebookName(serial):
    item = Engine.Items.GetItem(serial)

    if (item != None and item.Properties != None):
    	name = item.Properties[item.Properties.Length-1].Text
    	if name != "weight:" and name != "exceptional":
    		return name
    	else:
    		return ""

print "Target the runebook you wish to copy"
PromptAlias("bookToCopy")

more = ConfirmPrompt("Press OKAY and target a container inside your backpack with as many blank runebooks as copies you want to make.")

if more:
	PromptAlias("runebookBag")
	blankbooks = GetItemsInContainer(GetAlias("runebookBag"))
	Pause(1000)
else:
	Stop()
	
entries = GetRunebookEntries(GetAlias("bookToCopy"))
bookname = GetRunebookName(GetAlias("bookToCopy"))
runesneeded = len(entries)*len(blankbooks)
blankrunes = CountType(0x1f14, "backpack")

if blankrunes >= runesneeded:

	for x in range(len(entries)):
		SysMessage(entries[x])
		UseObject("bookToCopy")
		WaitForGump(0x554b87f3, 5000)
		while Mana() < 10:
			HeadMessage("Waiting for mana", "self", 33)
			Pause(5000)
		ReplyGump(0x554b87f3, recallbuttons[x])
		if InJournal("blocked", "system"):
			HeadMessage("Waiting to try again", "self", 33)
			Pause(10000)
			ReplyGump(0x554b87f3, recallbuttons[x])
		ClearJournal()
		Pause(5000)
		for y in range(len(blankbooks)):
			if FindType(0x1f14, -1, "backpack"):
				SysMessage(str(GetAlias("found")))
				while Mana() < 17:
					HeadMessage("Waiting for mana", "self", 33)
					Pause(5000)
				Cast("Mark", "found")
				Pause(2000)
				UseObject("found")
				WaitForPrompt(5000)
				PromptMsg(entries[x])        
				Pause(1000)
				MoveItem("found", blankbooks[y])
				Pause(3000)
			else:
				SysMessage("Out of runes! Stopping", 33)
				Stop()
				
	if bookname != "":
		for i in range(len(blankbooks)):
			UseObject(blankbooks[i])
			WaitForGump(0x554b87f3, 5000)
			ReplyGump(0x554b87f3, 1)
			WaitForPrompt(5000)
			PromptMsg(bookname)
			ReplyGump(0x554b87f3, 0)
			Pause(1000)
		
	SysMessage("Finished", 33)
	
else:

	SysMessage("Not enough runes! Stopping", 33)
	Stop()