# Name: Scroll Maker
# Description: Crafts selected scrolls up to selected amount. Read instructions
# Author: Kakagriss
# Shard: UOG-Demise
# Date: Sun Mar 06 2022

# Instructions: You will need a container with regs, blank scrolls and iron ingots, and at least 1 tinker tool in your backpack.
# if you use a commodity deed box as a container and you put commodity deeds in, it will use them, but it's not neccesary for the script to work.
# make your selection and when you're ready press cancel when it asks you if you want to add more. Happy scribing!

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine

makeMax = 60000
makeCount = 0
craftGumpId = 0x38920abd

if not FindAlias('ScrollChest'):
	PromptMacroAlias('ScrollChest')
	
UseObject('ScrollChest')
WaitForContents('ScrollChest',3000)

def Tinker(category, button):
	count = CountType(0x1bf2, "backpack", 0)
	
	if count < 50:
		MoveType(0x1bf2, 'ScrollChest', "backpack", -1, -1, -1, 0, 50)
		Pause(1500)
		
	if FindType(0x1eb8, 0, "backpack"):
		UseObject("found")
		WaitForGump(craftGumpId, 5000)
		ReplyGump(craftGumpId, category)
		WaitForGump(craftGumpId, 5000)
		ReplyGump(craftGumpId, button)
		WaitForGump(craftGumpId, 5000)
	else:
		SysMessage("Out of tinker tools!", 33)
		Stop()

class ScrollInfo:
	def __init__(self, name, itemid, gumpButton1, gumpButton2, reagent, reagent2, reagent3, reagent4):
		self.name = name
		self.itemid = itemid
		self.gumpButton1 = gumpButton1
		self.gumpButton2 = gumpButton2
		self.reagent = reagent
		self.reagent2 = reagent2
		self.reagent3 = reagent3
		self.reagent4 = reagent4

ScrollInfo = [
	ScrollInfo("Reactive Armor", 0x1f2d, 1, 2, 0xf84, 0xf8d, 0xf8c, None),
	ScrollInfo("Magic Trap", 0x1f39, 8, 30, 0xf84, 0xf8d, 0xf8c, None),
	ScrollInfo("Protection", 0x1f3b, 8, 44, 0xf84, 0xf85, 0xf8c, None),
	ScrollInfo("Teleport", 0x1f42, 15, 37, 0xf7b, 0xf86, None, None),
	ScrollInfo("Curse", 0x1f47, 22, 16, 0xf84, 0xf88, 0xf8c, None),
	ScrollInfo("Recall", 0x1f4c, 22, 51, 0xf7a, 0xf7b, 0xf86, None),
	ScrollInfo("Magic Reflection", 0x1f50, 29, 23, 0xf84, 0xf86, 0xf8d, None),
	ScrollInfo("Paralyze", 0x1f52, 29, 37, 0xf84, 0xf86, 0xf8d, None),
	ScrollInfo("Energy Bolt", 0x1f56, 36, 9, 0xf7a, 0xf88, None, None),
	ScrollInfo("Explosion", 0x1f57, 36, 16, 0xf7b, 0xf86, None, None),
	ScrollInfo("Mass Curse", 0x1f5a, 36, 37, 0xf84, 0xf86, 0xf88, 0xf8c),
	ScrollInfo("Paralyze Field", 0x1f5b, 36, 44, 0xf7a, 0xf85, 0xf8d, None),
	ScrollInfo("Flamestrike", 0x1f5f, 43, 16, 0xf8d, 0xf8c, None, None),
	ScrollInfo("Meteor Swarm", 0x1f63, 43, 44, 0xf7b, 0xf86, 0xf8c, 0xf8d),
	ScrollInfo("Gate Travel", 0x1f60, 43, 23, 0xf7a, 0xf86, 0xf8c, None),
	ScrollInfo("Energy Field", 0x1f5e, 43, 9, 0xf7a, 0xf86, 0xf8d, 0xf8c),
	ScrollInfo("Mass Dispel", 0x1f62, 43, 37, 0xf7a, 0xf84, 0xf86, 0xf8c),
	ScrollInfo("Resurrection", 0x1f67, 50, 16, 0xf7b, 0xf84, 0xf85, None),
	ScrollInfo("Energy Vortex", 0x1f66, 50, 9, 0xf7a, 0xf7b, 0xf86, 0xf88),
	ScrollInfo("Curse Weapon", 0x2263, 57, 23, 0xf8a, None, None, None),
	ScrollInfo("Corpse Skin", 0x2262, 57, 16, 0xf78, 0xf8f, None, None),
	ScrollInfo("Blood Oath", 0x2261, 57, 9, 0xf7d, None, None, None),
	ScrollInfo("Evil Omen", 0x2264, 57, 30, 0xf78, 0xf8e, None, None),
	ScrollInfo("Pain Spike", 0x2268, 57, 58, 0xf8f, 0xf8a, None, None),
	ScrollInfo("Mind Rot", 0x2267, 57, 51, 0xf78, 0xf7d, 0xf8a, None),
	ScrollInfo("Poison Strike", 0x2269, 57, 65, 0xf8e, None, None, None),
	ScrollInfo("Wither", 0x226e, 57, 100, 0xf8f, 0xf8e, 0xf8a, None),
	ScrollInfo("Strangle", 0x226a, 57, 72, 0xf7d, 0xf8e, None, None),
	ScrollInfo("Vengeful Spirit", 0x226d, 57, 93, 0xf78, 0xf8f, 0xf8a, None)
]

scrolllist = []
nameslist = []
amountslist = []

(res, selection) = SelectionPrompt(ScrollInfo.Select(lambda i: i.name), "Which type of scroll would you like to make?")

if not res:
	Stop()

info = ScrollInfo[selection]
	
scrolllist.append(info)
nameslist.append(info.name)
print "Scrolls to make: " + str(nameslist)

(res, name) = MessagePrompt("How many?", str(makeMax))

if not res:
	Stop()

makeMax = int(name)
amountslist.append(makeMax)

while True:

	more = ConfirmPrompt("Do you want to make more?")
	
	if more:
		(res, selection) = SelectionPrompt(ScrollInfo.Select(lambda i: i.name), "Which type of scroll would you like to make?")

		if not res:
			Stop()

		info = ScrollInfo[selection]
	
		scrolllist.append(info)
		nameslist.append(info.name)
		print "Scrolls to make: " + str(nameslist)
		
		(amn, name) = MessagePrompt("How many?", str(makeMax))

		if not amn:
			Stop()

		makeMax = int(name)
		amountslist.append(makeMax)
		
	else:
		break
	

for i in range(0, len(scrolllist)):

	makeCount = CountType(scrolllist[i].itemid, "backpack")
	makeCount = makeCount + CountType(scrolllist[i].itemid, GetAlias('ScrollChest'))

	while makeCount < amountslist[i]:
	
		# Iron ingots
		countingots = CountType(0x1bf2, "backpack", 0)
		countingotscont = CountType(0x1bf2, 'ScrollChest', 0)
		
		# Reagents
		count = CountType(scrolllist[i].reagent, "backpack")
		if count < 100:
			MoveType(scrolllist[i].reagent, GetAlias('ScrollChest'), "backpack", -1, -1, -1, 0, 100)
			Pause(1000)
	
		if scrolllist[i].reagent2 != None:
			count2 = CountType(scrolllist[i].reagent2, "backpack")
			if count2 < 100:
				MoveType(scrolllist[i].reagent2, GetAlias('ScrollChest'), "backpack", -1, -1, -1, 0, 100)
				Pause(1000)
				
		if scrolllist[i].reagent3 != None:
			count3 = CountType(scrolllist[i].reagent3, "backpack")
			if count3 < 100:
				MoveType(scrolllist[i].reagent3, GetAlias('ScrollChest'), "backpack", -1, -1, -1, 0, 100)
				Pause(1000)

		if scrolllist[i].reagent4 != None:
			count4 = CountType(scrolllist[i].reagent4, "backpack")
			if count4 < 100:
				MoveType(scrolllist[i].reagent4, GetAlias('ScrollChest'), "backpack", -1, -1, -1, 0, 100)
				Pause(1000)
	
		# Tinker Tools
		counttitool = CountType(0x1eb8, 'backpack')
		
		if counttitool < 3:
			if countingots == 0 and countingotscont == 0:
				SysMessage("Out of ingots!", 33)
				Stop()
			else:
				Tinker(8, 23)
	
		# Scribe pen
		counttool = CountType(0xfbf, 'backpack')

		if counttool < 3:
			if countingots == 0 and countingotscont == 0:
				SysMessage("Out of ingots!", 33)
				Stop()
			else:
				Tinker(8, 156)
				
		# Blank scrolls
		countblank = CountType(0xef3, 'backpack')
		
		if countblank < 20:
			MoveType(0xef3, GetAlias('ScrollChest'), 'backpack', -1, -1, -1, 0, 20)
			Pause(1000)
		
		UseType(0xfbf)
		WaitForGump(craftGumpId, 5000)
		ReplyGump(craftGumpId, scrolllist[i].gumpButton1)
		WaitForGump(craftGumpId, 5000)
		ReplyGump(craftGumpId, scrolllist[i].gumpButton2)
		WaitForGump(craftGumpId, 5000)
	
		res,gump = Engine.Gumps.GetGump(craftGumpId)
	
		if res:
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 501629, Text: You inscribe the spell and put the scroll in your backpack.
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 502925, Text: You don't have the resources required to make that item.
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 1044378, Text: You do not have enough blank scrolls to make that.
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 1044153, Text: You don't have the required skills to attempt this item.
			ele = gump.Pages[0].GetElementByXY(170, 295)
		
			if ele != None and ele.Cliloc == 501629:
				makeCount = makeCount + 1
			else:
				if ele.Cliloc == 502925:
					SysMessage("Out of reagents!", 33)
					Stop()
				elif ele.Cliloc == 1044378:
					SysMessage("Out of blank scrolls!", 33)
					Stop()
				elif ele.Cliloc == 1044153:
					SysMessage("Not enough skill!", 33)
					Stop()
				else:
					if Mana() < 30:
						SysMessage("Not enough mana!", 33)
						if Skill("Meditation") > 50:
							print "Using Meditation"
							while not InJournal("enter a meditative trance", "system"):
								UseSkill("Meditation")
								Pause(10000)
							ClearJournal()
							while Mana() < MaxMana():
								Pause(100)
						else:
							print "Waiting for mana"
							while Mana() < MaxMana():
								Pause(100)						
				
		print scrolllist[i].name + ": " + str(makeCount)
			
		if Weight() > MaxWeight() - 80:
			MoveType(scrolllist[i].itemid, "backpack", GetAlias('ScrollChest'))
			Pause(1000)
		
	Pause(1000)		
	MoveType(scrolllist[i].itemid, "backpack", GetAlias('ScrollChest'))
	Pause(1000)
	deedCount = CountType(0x14f0, 'ScrollChest', 71)
	if FindType(scrolllist[i].itemid, -1, 'ScrollChest'):
		scrolls = GetAlias("found")

	if deedCount > 0:
		UseType(0x14f0, 71, 'ScrollChest')
		WaitForTarget(5000)
		Target(scrolls)
		print Name(scrolls) + " turned into deed"
	else:
		SysMessage("Out of commodity deeds!", 33)
	
SysMessage("Finished", 33)