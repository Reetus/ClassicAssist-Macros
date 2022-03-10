# Name: Potion Maker
# Description: Crafts selected potions up to selected amounts
# Author: Kakagriss
# Shard: UOG-Demise
# Date: Fri Mar 04 2022

# This is just a modified version of 'Potion Factory' by Reetus. All credits to him.

# Instructions: You will need a container with regs, empty bottles and iron ingots, and at least 1 tinker tool in your backpack.
# make sure you have tinkering to make tools. If you use a commodity deed box as a container and you put commodity deeds in, it will use them,
# but it's not neccesary for the script to work. Make your selection and when you're ready press cancel when it asks you if you want to add more.
# Happy brewing!

import clr
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
from Assistant import Engine

makeMax = 60000
makeCount = 0
craftGumpId = 0x38920abd

if not FindAlias('PotionChest'):
	PromptMacroAlias('PotionChest')
	
UseObject('PotionChest')
WaitForContents('PotionChest',3000)

def Tinker(category, button):
	count = CountType(0x1bf2, "backpack", 0)
	
	if count < 50:
		MoveType(0x1bf2, 'PotionChest', "backpack", -1, -1, -1, 0, 50)
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

class PotionInfo:
	def __init__(self, name, itemid, hue, gumpButton1, gumpButton2, reagent, reagent2):
		self.name = name
		self.itemid = itemid
		self.hue = hue
		self.gumpButton1 = gumpButton1
		self.gumpButton2 = gumpButton2
		self.reagent = reagent
		self.reagent2 = reagent2

potionInfo = [
	PotionInfo("Greater Cure", 0xf07, 0, 43, 16, 0xf84, None),
	PotionInfo("Greater Heal", 0xf0c, 0, 22, 16, 0xf85, None),
	PotionInfo("Deadly Poison", 0xf0a, 0, 36, 23, 0xf88, None),
	PotionInfo("Greater Refreshment", 0xf0b, 0, 1, 9, 0xf7a, None),
	PotionInfo("Greater Strength", 0xf09, 0, 29, 9, 0xf86, None),
	PotionInfo("Greater Agility", 0xf08, 0, 8, 9, 0xf7b, None),
	PotionInfo("Greater Explosion", 0xf0d, 0, 50, 16, 0xf8c, None),
	PotionInfo("Greater Conflagration", 0xf06, 1161, 57, 9, 0xf8f, None),
	PotionInfo("Greater Confusion Blast", 0xf06, 1165, 57, 23, 0xf8a, None),
	PotionInfo("Parasitic Poison", 0xf0a, 380, 36, 30, 0x3190, None),
	PotionInfo("Darkglow Poison", 0xf0a, 150, 36, 37, 0x3191, None),
	PotionInfo("Invisibility", 0xf06, 306, 64, 2, 0xf7b, 0xf88),
	PotionInfo("Smoke Bomb", 0x2808, 0, 50, 23, 0xf85, 0x9b5),
]

potionlist = []
nameslist = []
amountslist = []

(res, selection) = SelectionPrompt(potionInfo.Select(lambda i: i.name), "Which type of potion would you like to make?")

if not res:
	Stop()

info = potionInfo[selection]
	
potionlist.append(info)
nameslist.append(info.name)
print "Potions to make: " + str(nameslist)

(res, name) = MessagePrompt("How many?", str(makeMax))

if not res:
	Stop()

makeMax = int(name)
amountslist.append(makeMax)

while True:

	more = ConfirmPrompt("Do you want to make more?")
	
	if more:
		(res, selection) = SelectionPrompt(potionInfo.Select(lambda i: i.name), "Which type of potion would you like to make?")

		if not res:
			Stop()

		info = potionInfo[selection]
	
		potionlist.append(info)
		nameslist.append(info.name)
		print "Potions to make: " + str(nameslist)
		
		(amn, name) = MessagePrompt("How many?", str(makeMax))

		if not amn:
			Stop()

		makeMax = int(name)
		amountslist.append(makeMax)
		
	else:
		break
	

for i in range(0, len(potionlist)):

	makeCount = CountType(potionlist[i].itemid, "backpack", potionlist[i].hue)
	makeCount = makeCount + CountType(potionlist[i].itemid, GetAlias('PotionChest'), potionlist[i].hue)

	while makeCount < amountslist[i]:
		# Iron ingots
		countingots = CountType(0x1bf2, "backpack", 0)
		countingotscont = CountType(0x1bf2, 'PotionChest', 0)
		
		# Reagent
		count = CountType(potionlist[i].reagent, "backpack")
		
		if count < 100:
			MoveType(potionlist[i].reagent, GetAlias('PotionChest'), "backpack", -1, -1, -1, 0, 100)
			Pause(1000)
	
		# Reagent 2
		if potionlist[i].reagent2 != None:
			count = CountType(potionlist[i].reagent2, "backpack")
			if count < 100:
				MoveType(potionlist[i].reagent2, GetAlias('PotionChest'), "backpack", -1, -1, -1, 0, 100)
				Pause(1000)
	
		# Tinker Tools
		count = CountType(0x1eb8, 'backpack')
		
		if count < 3:
			if countingots == 0 and countingotscont == 0:
				SysMessage("Out of ingots!", 33)
				Stop()
			else:
				Tinker(8, 23)
	
		# Mortar and pestal
		count = CountType(0xe9b, 'backpack')

		if count < 3:
			if countingots == 0 and countingotscont == 0:
				SysMessage("Out of ingots!", 33)
				Stop()
			else:
				Tinker(8, 9)
				
		# Bottles
		if potionlist[i].reagent2 != 0x9b5:
			count = CountType(0xf0e, 'backpack')
		
			if count < 20:
				MoveType(0xf0e, GetAlias('PotionChest'), 'backpack', -1, -1, -1, 0, 20)
				Pause(1000)
		
		UseType(0xe9b)
		WaitForGump(craftGumpId, 5000)
		ReplyGump(craftGumpId, potionlist[i].gumpButton1)
		WaitForGump(craftGumpId, 5000)
		ReplyGump(craftGumpId, potionlist[i].gumpButton2)
		WaitForGump(craftGumpId, 5000)
	
		res,gump = Engine.Gumps.GetGump(craftGumpId)
	
		if res:
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 500279, Text: You pour the potion into a bottle...
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 502925, Text: You don't have the resources required to make that item.
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 1044154, Text: You create the item.
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 500315, Text: You need an empty bottle to make a potion.
			#X: 170, Y: 295, Type: xmfhtmlgumpcolor, Cliloc: 1044153, Text: You don't have the required skills to attempt this item.
			ele = gump.Pages[0].GetElementByXY(170, 295)
		
			if ele != None and (ele.Cliloc == 500279 or ele.Cliloc == 1044154):
				makeCount = makeCount + 1
			else:
				if ele.Cliloc == 502925:
					SysMessage("Out of reagents!", 33)
					Stop()
				if ele.Cliloc == 500315:
					SysMessage("Out of empty bottles!", 33)
					Stop()
				if ele.Cliloc == 1044153:
					SysMessage("Not enough skill!", 33)
					Stop()
				
		print potionlist[i].name + ": " + str(makeCount)
			
		if Weight() > MaxWeight() - 80:
			MoveType(potionlist[i].itemid, "backpack", GetAlias('PotionChest'))
			Pause(1000)
		
	Pause(1000)		
	MoveType(potionlist[i].itemid, "backpack", GetAlias('PotionChest'))
	Pause(1000)
	deedCount = CountType(0x14f0, 'PotionChest', 71)
	if FindType(potionlist[i].itemid, -1, 'PotionChest', potionlist[i].hue):
		pots = GetAlias("found")

	if deedCount > 0:
		UseType(0x14f0, 71, 'PotionChest')
		WaitForTarget(5000)
		Target(pots)
		print Name(pots) + " turned into deed"
	else:
		SysMessage("Out of commodity deeds!", 33)
	
SysMessage("Finished", 33)