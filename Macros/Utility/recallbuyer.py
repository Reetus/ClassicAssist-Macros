# Name: Recall Buyer
# Description: Buys everything in your active AutoBuy agent and goes through given runebooks. Read instructions.
# Author: Kakagriss
# Shard: UOG-Demise
# Date: Wed Mar 02 2022

# Instructions: You will need a runebook with the first rune being your dropoff location, where you should have a container.
# replace the serials below for these items, as well as for your vendor runebooks. You can use as many as you want with as many runes as you want.
# you also need a pet with a backpack. Setup your AutoBuy agent and copy the graphics below. It will wait 1 hour and go at it again.
# loop and play. Happy buying! 

from Assistant import Engine
import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)

recallbuttons = [5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95]	
runebooks = [0x42814728] #Replace this with your own runebooks
homebook = 0x4281394f #Replace this with your own runebook with dropoff location
resChest = 0x41ca1929 #Replace this with your resource container
stuff = [0xef3, 0x1bf2] #Replace this with the graphics on your AutoBuy agent

if Mounted("self"):
	UseObject("self")
	Msg("All follow me")
	Pause(100)
	
if not FindAlias("cargopet"):
	PromptAlias("cargopet")
	
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

def GetMobiles(ids = None, notorieties = None, includeFriends = False, includeIgnored = False, maxDistance = 32, orderBy = lambda m: m.Distance):
	mobiles = Engine.Mobiles.Where(lambda m: (ids == None or ids.Contains(m.ID))
                                             	and m.Distance < maxDistance
                                             	and m.Serial != Engine.Player.Serial
                                             	and not Property(m, "Instructor")
                                             	and (notorieties == None or notorieties.Contains(m.Notoriety.ToString()))
						and (includeFriends or not InFriendList(m.Serial))
						and (includeIgnored or not InIgnoreList(m.Serial))).OrderBy(orderBy)
	return mobiles

def OverloadToPet(pet):
	if Weight() >= MaxWeight() - 150:
		for item in stuff:
			while FindType(item, -1, "backpack"):
				MoveItem("found", pet)
				Pause(1000)
			while FindType(item, 3):
				MoveItem("found", "backpack")
				Pause(1000)
			
def DropResources(runebook):
	UseObject(runebook)
	WaitForGump(0x554b87f3, 5000)
	ReplyGump(0x554b87f3, 5)
	Pause(5000)
	for item in stuff:
		while FindType(item, -1, "backpack"):
			MoveItem("found", resChest)
			Pause(1000)
		while FindType(item, -1, "cargopet"):
			MoveItem("found", resChest)
			Pause(1000)			

if not TimerExists("buytime"):
	CreateTimer("buytime")
	
for y in range(len(runebooks)):
	currentbook = runebooks[y]
	entries = GetRunebookEntries(currentbook)
	for x in range(len(entries)):
		UseObject(currentbook)
		WaitForGump(0x554b87f3, 5000)
		ReplyGump(0x554b87f3, recallbuttons[x])
		Pause(5000)
		mobiles = GetMobiles(maxDistance = 12, notorieties = ["Invulnerable"]).Select(lambda m: m.Serial)
		for m in mobiles:
			if Property(m, "blacksmith") or Property(m, "tailor") or Property(m, "weaver") or Property(m, "weaponsmith") and not Property(m, "Guildmaster") and not Property(m, "Guildmistress"):
				HeadMessage(Name(m),m)
				WaitForContext(m, 2, 5000)
				Pause(1000)
			else:
				HeadMessage(Name(m),m)
				WaitForContext(m, 1, 5000)
				Pause(1000)
			SetTimer("buytime", 0)
			for item in stuff:
				while FindType(item, 3):
					MoveItem("found", "cargopet")
					Pause(1000)
			OverloadToPet("cargopet")
			if Weight() >= MaxWeight() - 80:
				DropResources(homebook)
				UseObject(currentbook)
				WaitForGump(0x554b87f3, 5000)
				ReplyGump(0x554b87f3, recallbuttons[x])
				Pause(5000)
				
DropResources(homebook)
print "NOW WAITING"
while Timer("buytime") < 3600000:
	Pause(100)